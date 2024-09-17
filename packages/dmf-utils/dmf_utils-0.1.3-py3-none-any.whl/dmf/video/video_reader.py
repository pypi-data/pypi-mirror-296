from pathlib import Path
from typing import Union, List, Literal, Iterator

try:
    import cv2
except ImportError:
    raise ImportError(
        "OpenCV is required for video reading. "
        "Install it using `pip install opencv-python`."
    )

try:
    import numpy as np
except ImportError:
    raise ImportError(
        "NumPy is required for video reading. "
        "Install it using `pip install numpy`."
    )

from PIL import Image

__all__ = ["read_video", "VideoReader"]

OutputType = Literal["numpy", "pil"]


def read_video(
    file_path: Union[str, Path], 
    output_type: OutputType = "numpy"
) -> Union[np.ndarray, List[Image.Image]]:
    """
    Read an entire video and return the frames as either NumPy arrays or PIL images.

    Parameters
    ----------
    file_path : Union[str, Path]
        The path to the input video file.
    output_type : Literal["numpy", "pil"], default="numpy"
        The desired output type for the frames. "numpy" returns frames as NumPy arrays,
        while "pil" returns frames as PIL images.

    Returns
    -------
    Union[np.ndarray, List[Image.Image]]
        A NumPy array of shape (num_frames, height, width, 3) if output_type is "numpy",
        or a list of PIL images if output_type is "pil".
    """
    with VideoReader(file_path, output_type=output_type) as reader:
        return reader.read_video()


class VideoReader:
    """
    A utility class to read videos and return frames as either NumPy arrays or PIL images.

    Parameters
    ----------
    file_path : Union[str, Path]
        The path to the input video file.
    output_type : Literal["numpy", "pil"], default="numpy"
        The desired output type for the frames. "numpy" returns frames as NumPy arrays,
        while "pil" returns frames as PIL images.
    
    Examples
    --------
    Reading the entire video as NumPy arrays:

    .. code-block:: python

        reader = VideoReader("input.mp4", output_type="numpy")
        frames = reader.read_video()

    Iterating over video frames as PIL images:

    .. code-block:: python

        reader = VideoReader("input.mp4", output_type="pil")
        for frame in reader:
            frame.show()  # Display the frame using PIL's show method

    Accessing a specific frame by index:

    .. code-block:: python

        reader = VideoReader("input.mp4", output_type="numpy")
        frame = reader[10]  # Get the 11th frame (index starts at 0)
    """

    def __init__(self, file_path: Union[str, Path], output_type: OutputType = "numpy"):
        self.file_path = Path(file_path)
        self.output_type = output_type
        self._cap = None
        self._frame_count = 0
        self._initialize_reader()

    def _initialize_reader(self):
        """Initialize the video reader."""
        self._cap = cv2.VideoCapture(str(self.file_path))
        if not self._cap.isOpened():
            raise FileNotFoundError(f"Unable to open video file: {self.file_path}")
        self._frame_count = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def read_video(self) -> Union[np.ndarray, List[Image.Image]]:
        """
        Read the entire video and return all frames.

        Returns
        -------
        Union[np.ndarray, List[Image.Image]]
            A NumPy array of shape (num_frames, height, width, 3) if output_type is "numpy",
            or a list of PIL images if output_type is "pil".
        """
        frames = []
        while True:
            ret, frame = self._cap.read()
            if not ret:
                break
            frames.append(self._process_frame(frame))

        self._cap.release()

        if self.output_type == "numpy":
            return np.array(frames)
        return frames

    def _process_frame(self, frame: np.ndarray) -> Union[np.ndarray, Image.Image]:
        """Convert the frame to the desired output type."""
        if self.output_type == "pil":
            return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        return frame

    def __getitem__(self, index: int) -> Union[np.ndarray, Image.Image]:
        """
        Retrieve a specific frame by index.

        Parameters
        ----------
        index : int
            The index of the frame to retrieve (0-based).

        Returns
        -------
        Union[np.ndarray, Image.Image]
            The frame at the specified index.
        """
        if index < 0 or index >= self._frame_count:
            raise IndexError("Frame index out of range")

        self._cap.set(cv2.CAP_PROP_POS_FRAMES, index)
        ret, frame = self._cap.read()
        if not ret:
            raise ValueError(f"Failed to retrieve frame at index {index}")

        return self._process_frame(frame)

    def __iter__(self) -> Iterator[Union[np.ndarray, Image.Image]]:
        """
        Iterate over video frames one by one.

        Yields
        ------
        Union[np.ndarray, Image.Image]
            The next frame in the video as either a NumPy array or a PIL image.
        """
        self._initialize_reader()
        return self

    def __next__(self) -> Union[np.ndarray, Image.Image]:
        """
        Return the next frame in the video.

        Returns
        -------
        Union[np.ndarray, Image.Image]
            The next frame in the video as either a NumPy array or a PIL image.

        Raises
        ------
        StopIteration
            If the video has no more frames.
        """
        if not self._cap.isOpened():
            raise StopIteration

        ret, frame = self._cap.read()
        if not ret:
            self._cap.release()
            raise StopIteration

        return self._process_frame(frame)

    def __len__(self) -> int:
        """Return the total number of frames in the video."""
        return self._frame_count

    def __enter__(self):
        """Context management enter method."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Context management exit method."""
        if self._cap:
            self._cap.release()
