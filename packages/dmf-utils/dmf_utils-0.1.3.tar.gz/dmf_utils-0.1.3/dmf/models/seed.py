import random
import numpy as np
import torch

def set_seed(seed: int) -> "torch.Generator":
    """
    Set the seed for random number generation in Python, NumPy, and PyTorch to ensure reproducibility.

    Parameters
    ----------
    seed : int
        The seed value to set for random number generation.

    Returns
    -------
    torch.Generator
        The random number generator for PyTorch.
    """
    # Set the seed for Python's built-in random module
    random.seed(seed)

    # Set the seed for NumPy
    np.random.seed(seed)

    # Set the seed for PyTorch based on the available device
    if torch.cuda.is_available():
        # Set seed for CUDA devices
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)  # For multi-GPU setups
        rg = torch.Generator(torch.cuda.current_device())
    else:
        # Set seed for CPU-only and MPS, since it's a CPU-based backend
        torch.manual_seed(seed)
        rg = torch.Generator()

    # Ensure deterministic behavior in cuDNN (if applicable)
    if torch.backends.cudnn.is_available():
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    rg.manual_seed(seed)
    return rg
