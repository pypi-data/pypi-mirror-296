from pathlib import Path
from typing import Optional, Union, Callable, List

__all__ = ["load", "register_loader"]

# Loaders and extension mapping
LOADERS = {}
EXTENSION_MAPPING = {}

def load(file_path: Union[str, Path], loader: Optional[str] = None, **kwargs):
    """
    Load data from a file using the appropriate loader.

    This function loads data from various file formats by automatically determining the appropriate loader based on the file extension. You can also specify the loader explicitly if desired.

    Supported Loaders
    -----------------
    - "pickle": For .pkl files.
    - "joblib": For .joblib files.
    - "pandas": For .csv, .parquet, .xlsx, .xls, .feather files.
    - "json": For .json files.
    - "str": For .txt, .html, .log, .md, .rst files.
    - "hdf5": For .h5, .hdf5, .hdf files.
    - "numpy": For .npz, .npy files.
    - "pillow": For image files (.jpg, .jpeg, .png, .bmp, .gif, .tiff, .tif, .webp).
    - "pytorch": For PyTorch model files (.pt, .pth).
    - "yaml": For .yaml, .yml files.
    - "ini": For .ini, .cfg files.
    - "matlab": For .mat files.
    - "audio": For audio files (.wav, .mp3, .flac, .ogg).
    - "video": For video files (.mp4, .avi, .mov, .mkv).

    Parameters
    ----------
    file_path : Union[str, Path]
        The path to the file to load. The file extension will be used to determine the appropriate loader if not specified.
    loader : Optional[str], default=None
        The loader type to use. If not provided, it will be inferred from the file extension.
    kwargs : dict
        Additional keyword arguments to pass to the loader function.

    Returns
    -------
    Any
        The data loaded from the file. The return type depends on the loader used, such as:
        - pd.DataFrame for Pandas files (.csv, .parquet, etc.)
        - dict for JSON or YAML files
        - np.ndarray for NumPy files (.npy, .npz)
        - torch.Tensor for PyTorch model files (.pt, .pth)
        - PIL.Image for image files (.jpg, .png, etc.)
        - str for text files (.txt, .log, etc.)
        - configparser.ConfigParser for INI files
        - dict for MATLAB files (.mat)
        - tuple[np.ndarray, int] for audio files
        - list[np.ndarray] for video files
        - Any for pickle and joblib files (the specific type depends on the serialized object)

    Raises
    ------
    ValueError
        If the file extension or specified loader is not supported.
    ImportError
        If the required library for the specified loader is not installed.

    Examples
    --------
    Loading a DataFrame from a CSV file:

    .. code-block:: python

        import pandas as pd
        df = load('data.csv')
        type(df)
        # <class 'pandas.core.frame.DataFrame'>

    Loading an image using Pillow:

    .. code-block:: python

        img = load('image.png')
        type(img)
        # <class 'PIL.PngImagePlugin.PngImageFile'>

    Loading a PyTorch model:

    .. code-block:: python

        tensor = load('model.pth')
        type(tensor)
        # <class 'torch.Tensor'>
    """

    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"File '{file_path}' does not exist.")
    
    ext = file_path.suffix.lstrip(".").lower()
    if loader and loader not in LOADERS:
        raise ValueError(f"Loader '{loader}' is not supported. "
                         f"Use one of {list(LOADERS.keys())}.")
    elif not loader:
        loader = EXTENSION_MAPPING.get(ext, None)
        if not loader:
            raise ValueError(
                f"File extension '{ext}' is not supported. "
                f"Supported extensions: {list(EXTENSION_MAPPING.keys())}. "
                "Please specify a supported loader."
            )
    
    loader_func = LOADERS[loader]
    return loader_func(file_path, **kwargs)


def register_loader(loader_name: str, extensions: List[str]):
    """
    Decorator to register a custom loader.

    Parameters
    ----------
    loader_name : str
        The name of the loader (must be unique).
    extensions : List[str]
        The list of file extensions that the loader should handle (without leading dot).
    """
    def decorator(loader_function: Callable):
        # Register the loader function
        if loader_name in LOADERS:
            raise ValueError(f"Loader '{loader_name}' is already registered.")
        
        LOADERS[loader_name] = loader_function

        # Register the extensions
        for extension in extensions:
            EXTENSION_MAPPING[extension] = loader_name

        return loader_function
    return decorator


@register_loader("pickle", ["pkl", "pickle"])
def load_pickle(file_path: Path, **kwargs):
    """Load a file using the pickle loader."""
    import pickle
    with open(file_path, "rb") as file:
        return pickle.load(file, **kwargs)

@register_loader("joblib", ["joblib"])
def load_joblib(file_path: Path, **kwargs):
    """Load a file using the joblib loader."""
    try:
        import joblib
    except ImportError:
        raise ImportError("joblib package is required for joblib loading. "
                          "Install it using `pip install joblib`.")
    return joblib.load(file_path, **kwargs)

@register_loader("hdf5", ["h5", "hdf5", "hdf"])
def load_hdf5(file_path: Path, **kwargs):
    """Load a file using the hdf5 loader."""
    try:
        import h5py
    except ImportError:
        raise ImportError("h5py package is required for hdf5 loading. "
                          "Install it using `pip install h5py`.")
    with h5py.File(file_path, "r") as file:
        return file

@register_loader("json", ["json"])
def load_json(file_path: Path, **kwargs):
    """Load a file using the json loader."""
    import json
    with open(file_path, "r") as file:
        return json.load(file, **kwargs)
    
@register_loader("str", ["txt", "html", "log", "md", "rst"])
def txt_loader(file_path: Path, **kwargs):
    """Load a file using the txt loader."""
    with open(file_path, "r") as file:
        return file.read(**kwargs)

@register_loader("numpy", ["npz", "npy"])
def numpy_loader(file_path: Path, **kwargs):
    """Load a file using the numpy loader."""
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy package is required for numpy loading. "
                          "Install it using `pip install numpy`.")
    ext = file_path.suffix.lstrip(".").lower()
    if ext == "npz":
        return np.load(file_path, **kwargs)
    elif ext == "npy":
        return np.load(file_path, **kwargs)
    else:
        raise ValueError(f"Extension {ext} is not supported for numpy loading. "
                        f"Use one of {EXTENSION_MAPPING.keys()} or use directly the numpy loader.")

@register_loader("pandas", ["csv", "parquet", "xlsx", "xls", "feather"])
def pandas_loader(file_path: Path, **kwargs):
    """Load a file using the pandas loader."""
    import pandas as pd
    ext = file_path.suffix.lstrip(".").lower()
    if ext == "csv":
        return pd.read_csv(file_path, **kwargs)
    elif ext == "parquet":
        return pd.read_parquet(file_path, **kwargs)
    elif ext == "xlsx":
        return pd.read_excel(file_path, **kwargs)
    elif ext == "xls":
        return pd.read_excel(file_path, **kwargs)
    elif ext == "feather":
        return pd.read_feather(file_path, **kwargs)
    else:
        raise ValueError(f"Extension {ext} is not supported for pandas loading. "
                        f"Use one of {EXTENSION_MAPPING.keys()} or use directly the pandas loader.")
    
@register_loader("pillow", ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "tif", "webp"])
def pillow_loader(file_path: Path, **kwargs):
    """Load a file using the pillow loader."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow package is required for pillow loading. "
                          "Install it using `pip install pillow`.")
    return Image.open(file_path, **kwargs)

@register_loader("pytorch", ["pt", "pth"])
def pytorch_loader(file_path: Path, **kwargs):
    """Load a file using the pytorch loader."""
    try:
        import torch
    except ImportError:
        raise ImportError("torch package is required for pytorch loading. "
                          "Install it using `pip install torch`.")
    return torch.load(file_path, **kwargs)

@register_loader("yaml", ["yaml", "yml"])
def load_yaml(file_path: Path, **kwargs):
    """Load a file using the YAML loader."""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required to load .yaml files. "
                          "Install it using `pip install pyyaml`.")
    
    with open(file_path, "r") as file:
        return yaml.safe_load(file)


@register_loader("ini", ["ini", "cfg"])
def load_ini(file_path: Path, **kwargs):
    """Load a file using the INI loader."""
    import configparser    
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


@register_loader("matlab-scipy", ["mat"])
def load_matlab(file_path: Path, **kwargs):
    """Load a file using the MATLAB loader."""
    try:
        import scipy.io
    except ImportError:
        raise ImportError("scipy.io is required to load .mat files. "
                          "Install it using `pip install scipy`.")
    
    return scipy.io.loadmat(file_path, **kwargs)


@register_loader("audio-librosa", ["wav", "mp3", "flac", "ogg"])
def load_audio(file_path: Path, **kwargs):
    """Load a file using the audio loader."""
    try:
        import librosa
    except ImportError:
        raise ImportError("librosa is required to load audio files. "
                          "Install it using `pip install librosa`.")
    
    return librosa.load(file_path, **kwargs)


@register_loader("video-cv2", ["mp4", "avi", "mov", "mkv"])
def load_video(file_path: Path, **kwargs):
    """Load a file using the video loader."""
    try:
        import cv2
    except ImportError:
        raise ImportError("OpenCV is required to load video files. "
                          "Install it using `pip install opencv-python`.")
    
    cap = cv2.VideoCapture(str(file_path))
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames
