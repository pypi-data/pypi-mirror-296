import torch
import zhang_suen_thinning


def skeletonize(image: torch.Tensor) -> torch.Tensor:
    orig_shape = image.shape
    orig_dtype = image.dtype
    orig_max = torch.max(image)

    image = image.squeeze()
    if orig_max == 1:
        image = image * 255
    image = image.to(torch.uint8)

    result = zhang_suen_thinning.skeletonize(image)

    if orig_max <= 1:
        result = result // 255
    result = result.to(orig_dtype)
    if len(orig_shape) >= 3:
        result = result.reshape(orig_shape)
    return result
