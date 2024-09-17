# mypy: disable-error-code="valid-type"
from typing import Optional, Tuple

import torch
import warp as wp
from jaxtyping import Float


@wp.kernel
def axis_angle_to_matrix_via_quat_kernel(
    axis: wp.array(dtype=wp.vec3),
    angle: wp.array(dtype=wp.float32),
    rot_mat: wp.array(dtype=wp.mat33),
):
    tid = wp.tid()
    rot_mat[tid] = wp.quat_to_matrix(wp.quat_from_axis_angle(axis[tid], angle[tid]))


@wp.kernel
def axis_angle_to_matrix_kernel(
    axis: wp.array(dtype=wp.vec3),
    angle: wp.array(dtype=wp.float32),
    rot_mat: wp.array(dtype=wp.mat33),
):
    tid = wp.tid()

    axis_elem = axis[tid]
    x, y, z = axis_elem[0], axis_elem[1], axis_elem[2]
    s, c = wp.sin(angle[tid]), wp.cos(angle[tid])
    C = 1.0 - c

    xs, ys, zs = x * s, y * s, z * s
    xC, yC, zC = x * C, y * C, z * C
    xyC, yzC, zxC = x * yC, y * zC, z * xC

    rot_mat[tid] = wp.mat33(
        x * xC + c, xyC - zs, zxC + ys, xyC + zs, y * yC + c, yzC - xs, zxC - ys, yzC + xs, z * zC + c
    )


class AxisAngleToMatrix(torch.autograd.Function):
    @staticmethod
    def forward(
        ctx, axis: Float[torch.Tensor, "... 3"], angle: Float[torch.Tensor, "..."]
    ) -> Float[torch.Tensor, "... 3 3"]:
        axis_wp = wp.from_torch(axis.view(-1, 3), dtype=wp.vec3)
        angles_wp = wp.from_torch(angle.view(-1), dtype=wp.float32)
        rot_mat_wp = wp.empty(
            axis_wp.shape,
            dtype=wp.mat33,  # type: ignore
            device=axis_wp.device,
            requires_grad=axis_wp.requires_grad,
        )
        wp.launch(
            kernel=axis_angle_to_matrix_kernel,
            dim=(axis_wp.shape[0],),
            inputs=[axis_wp, angles_wp],
            outputs=[rot_mat_wp],
            device=axis_wp.device,
        )
        if axis.requires_grad or angle.requires_grad:
            ctx.axis_wp = axis_wp
            ctx.angles_wp = angles_wp
            ctx.rot_mat_wp = rot_mat_wp
        return wp.to_torch(rot_mat_wp).view(angle.shape + (3, 3))

    @staticmethod
    def backward(  # type: ignore
        ctx, rot_mat_grad: Float[torch.Tensor, "... 3 3"]
    ) -> Tuple[Optional[Float[torch.Tensor, "... 3"]], Optional[Float[torch.Tensor, "..."]]]:
        ctx.rot_mat_wp.grad = wp.from_torch(rot_mat_grad.contiguous().view(-1, 3, 3), dtype=wp.mat33)
        wp.launch(
            kernel=axis_angle_to_matrix_kernel,
            dim=(ctx.axis_wp.shape[0],),
            inputs=[ctx.axis_wp, ctx.angles_wp],
            outputs=[ctx.rot_mat_wp],
            adj_inputs=[ctx.axis_wp.grad, ctx.angles_wp.grad],
            adj_outputs=[ctx.rot_mat_wp.grad],
            adjoint=True,
            device=ctx.axis_wp.device,
        )
        axis_grad = wp.to_torch(ctx.axis_wp.grad).view(rot_mat_grad.shape[:-1]) if ctx.axis_wp.requires_grad else None
        angle_grad = (
            wp.to_torch(ctx.angles_wp.grad).view(rot_mat_grad.shape[:-2]) if ctx.angles_wp.requires_grad else None
        )
        return axis_grad, angle_grad


def axis_angle_to_matrix(
    axis: Float[torch.Tensor, "... 3"], angle: Float[torch.Tensor, "..."]
) -> Float[torch.Tensor, "... 3 3"]:
    """
    Converts axis angles to rotation matrices using Rodrigues formula.

    Args:
        axis (torch.Tensor): axis, the shape could be [..., 3].
        angle (torch.Tensor): angle, the shape could be [...].

    Returns:
        torch.Tensor: Rotation matrices [..., 3, 3].

    Example:
        >>> axis = torch.tensor([1.0, 0.0, 0.0])
        >>> angle = torch.tensor(0.5)
        >>> axis_angle_to_matrix(axis, angle)
        tensor([[ 1.0000,  0.0000,  0.0000],
                [ 0.0000,  0.8776, -0.4794],
                [ 0.0000,  0.4794,  0.8776]])
    """
    return AxisAngleToMatrix.apply(axis, angle)  # type: ignore


__all__ = ["axis_angle_to_matrix"]
