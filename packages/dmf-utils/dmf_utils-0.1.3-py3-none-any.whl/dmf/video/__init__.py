from typing import TYPE_CHECKING

import lazy_loader as lazy

submod_attrs = {
    "video_writer": ["VideoWriter", "write_video"],
    "video_reader": ["VideoReader", "read_video"],
}

__getattr__, __dir__, __all__ = lazy.attach(__name__, submod_attrs=submod_attrs)

if TYPE_CHECKING:
    from .video_writer import VideoWriter, write_video
    from .video_reader import VideoReader, read_video

__all__ = ["write_video", "read_video", "VideoWriter", "VideoReader"]
