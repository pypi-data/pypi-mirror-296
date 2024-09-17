
from typing import Optional, Union
try:
    import torch
except ImportError:
    raise ImportError("PyTorch is not installed. Please, "
                      "install a suitable version of PyTorch.")

def get_device(device: Optional[Union[str, torch.device]] = None) -> torch.device:
    """Return the specified device.

    Parameters
    ----------
    device : str or torch.device, optional
        The device to use. If None, the default device is selected.

    Returns
    -------
    torch.device
        The selected device.
    """

    if device is None:
        if torch.cuda.is_available():
            device = torch.device("cuda")
        elif torch.backends.mps.is_available():
            device = torch.device("mps")
        else:
            device = torch.device("cpu")
    else:
        device = torch.device(device)

    return device