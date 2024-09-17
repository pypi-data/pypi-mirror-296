import gc
from typing import Dict, Optional, Union, Any

try:
    import torch
except ImportError:
    raise ImportError("PyTorch is not installed. Please, "
                      "install a suitable version of PyTorch.")

from .device import get_device
from ..utils.format_bytes import bytes_to_human_readable

def free(*objects: Any) -> None:
    """
    Free the memory associated with the given objects, including PyTorch models, tensors, and other related objects.

    Parameters
    ----------
    *objects : Any
        The objects to free. Typically these are PyTorch models or tensors.

    Notes
    -----
    This function handles CPU, CUDA, and MPS tensors/models by setting gradients to None, deleting the objects,
    clearing the CUDA or MPS cache if necessary, and calling garbage collection.
    """
    for obj in objects:
        if isinstance(obj, torch.nn.Module):
            # Free the model parameters' gradients
            for param in obj.parameters():
                if param.grad is not None:
                    param.grad = None
            # Move the model to CPU before deleting (optional, depending on use case)
            obj.to('cpu')

        elif isinstance(obj, torch.Tensor):
            # Free the tensor memory
            if obj.grad is not None:
                obj.grad = None
            # Move tensor to CPU before deletion (optional)
            obj = obj.cpu()

        # Delete the object reference
        del obj

    # Handle CUDA and MPS cache clearing
    if torch.cuda.is_available():
        torch.cuda.ipc_collect()
        torch.cuda.empty_cache()

    # Explicitly run garbage collection to free up memory
    gc.collect()


def get_memory_stats(device: Optional[Union[str, torch.device]] = None, format_size: bool=False) -> Dict[str, Any]:
    """
    Get memory statistics for the specified device.

    Parameters
    ----------
    device : str or torch.device, optional
        The device to get memory statistics for. If None, automatically detects
        the available device (CUDA, MPS, or CPU).
    format_size : bool, optional
        Whether to format the memory sizes in human-readable format (KB, MB, GB, TB). Default is False.

    Returns
    -------
    dict
        A dictionary containing memory statistics: free, occupied, reserved, and device.
    """
    # Determine the device if not provided
    device = get_device(device)

    memory_stats = {"device": str(device)}

    try:
        if device.type == "cuda":
            # CUDA memory stats
            memory_stats["free"] = torch.cuda.memory_free(device)
            memory_stats["occupied"] = torch.cuda.memory_allocated(device)
            memory_stats["reserved"] = torch.cuda.memory_reserved(device)
        else:
            # CPU memory stats using psutil
            import psutil
            virtual_mem = psutil.virtual_memory()
            memory_stats["free"] = virtual_mem.available
            memory_stats["occupied"] = virtual_mem.total - virtual_mem.available
            memory_stats["reserved"] = virtual_mem.total

    except Exception:
        memory_stats["free"] = None
        memory_stats["occupied"] = None
        memory_stats["reserved"] = None

    if format_size:
        for key in ["free", "occupied", "reserved"]:
            memory_stats[key] = bytes_to_human_readable(memory_stats[key])

    return memory_stats

