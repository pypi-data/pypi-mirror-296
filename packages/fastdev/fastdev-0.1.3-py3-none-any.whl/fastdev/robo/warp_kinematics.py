# mypy: disable-error-code="valid-type"
from typing import TYPE_CHECKING, Optional, Tuple

import torch
import warp as wp
from jaxtyping import Float

if TYPE_CHECKING:
    from fastdev.robo.robot_model import RobotModel


@wp.func
def axis_angle_to_tf_mat(axis: wp.vec3, angle: wp.float32):
    x, y, z = axis[0], axis[1], axis[2]
    s, c = wp.sin(angle), wp.cos(angle)
    C = 1.0 - c

    xs, ys, zs = x * s, y * s, z * s
    xC, yC, zC = x * C, y * C, z * C
    xyC, yzC, zxC = x * yC, y * zC, z * xC

    # fmt: off
    return wp.mat44(
        x * xC + c, xyC - zs, zxC + ys, 0.0,
        xyC + zs, y * yC + c, yzC - xs, 0.0,
        zxC - ys, yzC + xs, z * zC + c, 0.0,
        0.0, 0.0, 0.0, 1.0,
    )
    # fmt: on


@wp.func
def axis_distance_to_tf_mat(axis: wp.vec3, distance: wp.float32):
    x, y, z = axis[0], axis[1], axis[2]
    # fmt: off
    return wp.mat44(
        1.0, 0.0, 0.0, distance * x,
        0.0, 1.0, 0.0, distance * y,
        0.0, 0.0, 1.0, distance * z,
        0.0, 0.0, 0.0, 1.0,
    )
    # fmt: on


@wp.kernel
def forward_kinematics_kernel(
    joint_values: wp.array(dtype=wp.float32),
    num_dofs: wp.int32,
    num_links: wp.int32,
    link_indices_topological_order: wp.array(dtype=wp.int32),
    link_joint_types: wp.array(dtype=wp.int32),
    link_joint_indices: wp.array(dtype=wp.int32),
    link_joint_origins: wp.array(dtype=wp.mat44),
    parent_link_indices: wp.array(dtype=wp.int32),
    joint_axes: wp.array(dtype=wp.vec3),
    link_poses: wp.array(dtype=wp.mat44),
):
    b_idx = wp.tid()
    joint_offset = wp.int32(b_idx * num_dofs)  # type: ignore
    link_offset = wp.int32(b_idx * num_links)  # type: ignore

    for link_index in range(link_indices_topological_order.shape[0]):
        joint_type = link_joint_types[link_index]
        if joint_type == -1:
            glb_joint_pose = wp.identity(n=4, dtype=wp.float32)  # type: ignore
        else:
            parent_link_index = parent_link_indices[link_index]
            parent_link_pose = link_poses[link_offset + parent_link_index]
            joint_index = link_joint_indices[link_index]
            if joint_type == 0:
                local_joint_tf = wp.identity(n=4, dtype=wp.float32)  # type: ignore
            elif joint_type == 1:  # prismatic
                joint_value = joint_values[joint_offset + joint_index]
                joint_axis = joint_axes[joint_index]
                local_joint_tf = axis_distance_to_tf_mat(joint_axis, joint_value)
            elif joint_type == 2:  # revolute
                joint_value = joint_values[joint_offset + joint_index]
                joint_axis = joint_axes[joint_index]
                local_joint_tf = axis_angle_to_tf_mat(joint_axis, joint_value)
            joint_origin = link_joint_origins[link_index]
            glb_joint_pose = (parent_link_pose @ joint_origin) @ local_joint_tf  # type: ignore
        link_poses[link_offset + link_index] = glb_joint_pose


class ForwardKinematics(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx, joint_values: Float[torch.Tensor, "b num_dofs"], robot_model: "RobotModel"
    ) -> Float[torch.Tensor, "b num_links 4 4"]:
        num_dofs = joint_values.shape[-1]
        num_links = len(robot_model.link_names)
        joint_values_wp = wp.from_torch(joint_values.contiguous().view(-1), dtype=wp.float32)
        link_poses_wp = wp.zeros(
            # NOTE we use joint_values instead of joint_values_wp
            (joint_values.shape[0] * num_links,),
            dtype=wp.mat44,  # type: ignore
            device=joint_values_wp.device,
            requires_grad=joint_values_wp.requires_grad,
        )
        link_indices_topological_order = wp.from_torch(
            robot_model.link_indices_topological_order.contiguous(), dtype=wp.int32
        )
        link_joint_types = wp.from_torch(robot_model.link_joint_types.contiguous(), dtype=wp.int32)
        link_joint_indices = wp.from_torch(robot_model.link_joint_indices.contiguous(), dtype=wp.int32)
        link_joint_origins = wp.from_torch(robot_model.link_joint_origins.contiguous(), dtype=wp.mat44)
        parent_link_indices = wp.from_torch(robot_model.parent_link_indices.contiguous(), dtype=wp.int32)
        joint_axes = wp.from_torch(robot_model.joint_axes.contiguous(), dtype=wp.vec3)

        wp.launch(
            kernel=forward_kinematics_kernel,
            dim=(joint_values.shape[0],),
            inputs=[
                joint_values_wp,
                num_dofs,
                num_links,
                link_indices_topological_order,
                link_joint_types,
                link_joint_indices,
                link_joint_origins,
                parent_link_indices,
                joint_axes,
            ],
            outputs=[link_poses_wp],
            device=joint_values_wp.device,
        )

        if joint_values.requires_grad:
            ctx.joint_values_wp = joint_values_wp
            ctx.link_poses_wp = link_poses_wp
            ctx.num_dofs = num_dofs
            ctx.num_links = num_links
            ctx.link_indices_topological_order = link_indices_topological_order
            ctx.link_joint_types = link_joint_types
            ctx.link_joint_indices = link_joint_indices
            ctx.link_joint_origins = link_joint_origins
            ctx.parent_link_indices = parent_link_indices
            ctx.joint_axes = joint_axes

        return wp.to_torch(link_poses_wp).view(joint_values.shape[:-1] + (num_links, 4, 4))

    @staticmethod
    def backward(  # type: ignore
        ctx, link_poses_grad: Float[torch.Tensor, "b num_links 4 4"]
    ) -> Tuple[Optional[Float[torch.Tensor, "b num_dofs"]], None]:
        if ctx.joint_values_wp.requires_grad:
            ctx.link_poses_wp.grad = wp.from_torch(link_poses_grad.contiguous().view(-1, 4, 4), dtype=wp.mat44)
            wp.launch(
                kernel=forward_kinematics_kernel,
                dim=(link_poses_grad.shape[0],),
                inputs=[
                    ctx.joint_values_wp,
                    ctx.num_dofs,
                    ctx.num_links,
                    ctx.link_indices_topological_order,
                    ctx.link_joint_types,
                    ctx.link_joint_indices,
                    ctx.link_joint_origins,
                    ctx.parent_link_indices,
                    ctx.joint_axes,
                ],
                outputs=[ctx.link_poses_wp],
                adj_inputs=[ctx.joint_values_wp.grad, ctx.num_dofs, ctx.num_links, None, None, None, None, None, None],
                adj_outputs=[ctx.link_poses_wp.grad],
                adjoint=True,
                device=ctx.joint_values_wp.device,
            )
            joint_values_grad = wp.to_torch(ctx.joint_values_wp.grad).view(link_poses_grad.shape[:-3] + (ctx.num_dofs,))
        else:
            joint_values_grad = None
        return joint_values_grad, None


def forward_kinematics(
    joint_values: Float[torch.Tensor, "b num_dofs"], robot_model: "RobotModel"
) -> Float[torch.Tensor, "b num_links 4 4"]:
    return ForwardKinematics.apply(joint_values, robot_model)  # type: ignore
