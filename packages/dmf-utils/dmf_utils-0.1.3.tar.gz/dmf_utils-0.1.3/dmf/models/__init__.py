from typing import TYPE_CHECKING

import lazy_loader as lazy

submod_attrs = {
    "memory": ["free", "get_memory_stats"],
    "seed": ["set_seed"],
    "device": ["get_device"],
}

__getattr__, __dir__, __all__ = lazy.attach(__name__, submod_attrs=submod_attrs)

if TYPE_CHECKING:
    from .memory import free, get_memory_stats
    from .seed import set_seed
    from .device import get_device

__all__ = ["free", "get_memory_stats", "set_seed", "get_device"]
