
from psychopy import monitors
from psychopy.monitors import Monitor
from typing import TYPE_CHECKING

__all__ = ["resolve_monitor", "Monitor"]

if TYPE_CHECKING:
    from .config import Config

DEFAULT_WIDTH = 1920
DEFAULT_HEIGHT = 1200
DEFAULT_DISTANCE = 50
DEFAULT_MONITOR_WIDTH = 50

def resolve_monitor(
    config: "Config",
    **kwargs,
) -> Monitor:
    """Set up the monitor."""
    info = detect_monitor_size(config)

    monitor = monitors.Monitor(info['name'], **kwargs)
    monitor.setSizePix((info["width"], info["height"]))
    monitor.setWidth(info["monitor_width"])
    monitor.setDistance(info["distance"])
    monitor.save()

    return monitor

def detect_monitor_size(config: "Config", idx: int = 0):

    # Load default values
    width = config.get("display.width", DEFAULT_WIDTH)
    height = config.get("display.height", DEFAULT_HEIGHT)
    distance = config.get("display.distance", DEFAULT_DISTANCE)
    monitor_width = config.get("display.monitor_width", DEFAULT_MONITOR_WIDTH)
    info = {}

    try:
        from screeninfo import get_monitors
        detected_monitors = get_monitors()
    except ImportError:
        detected_monitors = []
    
    if len(detected_monitors) > 0:
        monitor = detected_monitors[idx]
        info['name'] = monitor.name or "default"
        info['width'] = monitor.width or width
        info['height'] = monitor.height or height
    
    info.setdefault('name', "default")
    info.setdefault('width', width)
    info.setdefault('height', height)
    info.setdefault('distance', distance)
    info.setdefault('monitor_width', monitor_width)

    return info