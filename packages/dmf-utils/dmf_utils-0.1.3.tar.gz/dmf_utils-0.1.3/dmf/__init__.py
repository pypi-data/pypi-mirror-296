"""dmf utils package"""
from typing import TYPE_CHECKING
import lazy_loader as lazy

from .__version__ import __version__

subpackages = ["alerts", "io", "env", "video", "models"]

__getattr__, __dir__, __all__ = lazy.attach(__name__, subpackages)

if TYPE_CHECKING:
    from . import alerts
    from . import io
    from . import env
    from . import video
    from . import models

__all__ = ["__version__", "alerts", "io", "env", "video", "models"]

