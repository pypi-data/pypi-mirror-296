import numpy as np
import torch
from typing import Optional
from jaxtyping import Float, Int64

from fastdev.extension import FDEV_EXT

try:
    import fpsample

    FPSAMPLE_AVAILABLE = True
except ImportError:
    FPSAMPLE_AVAILABLE = False


def sample_farthest_points(
    points: Float[torch.Tensor, "*B N 3"], num_samples: int
) -> Int64[torch.Tensor, "*B num_samples"]:
    """Sample farthest points.

    Args:
        points (Tensor): input points in shape (B, N, 3) or (N, 3)
        num_samples (int): number of samples

    Returns:
        Tensor: indices of farthest points in shape (B, num_samples) or (num_samples,)
    """
    if points.dim() != 3 and points.dim() != 2:
        raise ValueError("points should be in shape (B, N, 3) or (N, 3).")

    is_batch_input = points.dim() == 3
    if not is_batch_input:
        points = points.unsqueeze(0)

    indices = FDEV_EXT.load_module("fastdev_sample_farthest_points").sample_farthest_points(
        points,
        torch.ones((points.shape[0],), dtype=torch.long, device=points.device) * points.shape[1],
        torch.ones((points.shape[0],), dtype=torch.long, device=points.device) * num_samples,
        torch.zeros((points.shape[0],), dtype=torch.long, device=points.device),
    )

    if not is_batch_input:
        return indices.squeeze(0)
    else:
        return indices


def sample_farthest_points_numpy(
    points: Float[np.ndarray, "N 3"], num_samples: int, start_idx: Optional[int] = None
) -> Int64[np.ndarray, "num_samples"]:  # noqa: F821
    """Sample farthest points using fpsample.

    Args:
        points (np.ndarray): input points in shape (N, 3)
        num_samples (int): number of samples

    Returns:
        np.ndarray: indices of farthest points in shape (num_samples,)
    """
    if not FPSAMPLE_AVAILABLE:
        raise ImportError("fpsample is not available, please install it via `pip install fpsample`.")

    return fpsample.bucket_fps_kdline_sampling(points, num_samples, h=3, start_idx=start_idx)  # type: ignore


__all__ = ["sample_farthest_points"]
