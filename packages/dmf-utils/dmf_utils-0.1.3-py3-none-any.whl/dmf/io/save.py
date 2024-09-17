from pathlib import Path
from typing import Any, Optional, Union, Callable, List

__all__ = ["save", "register_saver"]

# Savers and extension mapping
SAVERS = {}
EXTENSION_MAPPING = {}

def save(data: Any, file_path: Union[str, Path], saver: Optional[str] = None, **kwargs):
    """
    Save data to a file using the appropriate saver.

    This function saves data to various file formats by automatically determining the appropriate saver based on the file extension. You can also specify the saver explicitly if desired.

    Supported Savers
    ----------------
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
    data : Any
        The data to be saved. The type of data should match the saver being used.
    file_path : Union[str, Path]
        The path to the file where the data should be saved. The file extension will be used to determine the appropriate saver if not specified.
    saver : Optional[str], default=None
        The saver type to use. If not provided, it will be inferred from the file extension.
    kwargs : dict
        Additional keyword arguments to pass to the saver function.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If the file extension or specified saver is not supported, or if the data type does not match the expected type.
    ImportError
        If the required library for the specified saver is not installed.

    Examples
    --------
    Saving a DataFrame to a CSV file:

    .. code-block:: python

        import pandas as pd
        from dmf.io import save

        df = pd.DataFrame({"a": [1, 2, 3]})
        save(df, "data.csv")

    Saving an image using Pillow:

    .. code-block:: python

        from PIL import Image
        from dmf.io import save

        img = Image.new("RGB", (100, 100), color="red")
        save(img, "image.png")

    Saving a NumPy array to an NPZ file:

    .. code-block:: python

        import numpy as np
        from dmf.io import save

        arr = np.array([1, 2, 3])
        save(arr, "data.npz")
    """
    file_path = Path(file_path)
    ext = file_path.suffix.lstrip(".").lower()
    if saver and saver not in SAVERS:
        raise ValueError(f"Saver '{saver}' is not supported. "
                         f"Use one of {list(SAVERS.keys())}.")
    elif not saver:
        saver = EXTENSION_MAPPING.get(ext, None)
        if not saver:
            raise ValueError(
                f"File extension '{ext}' is not supported. "
                f"Supported extensions: {list(EXTENSION_MAPPING.keys())}. "
                "Please specify a supported saver."
            )
    
    saver_func = SAVERS[saver]
    return saver_func(data, file_path, **kwargs)


def register_saver(saver_name: str, extensions: List[str]):
    """
    Decorator to register a custom saver.

    Parameters
    ----------
    saver_name : str
        The name of the saver (must be unique).
    extensions : List[str]
        The list of file extensions that the saver should handle (without leading dot).
    """
    def decorator(saver_function: Callable):
        # Register the saver function
        if saver_name in SAVERS:
            raise ValueError(f"Saver '{saver_name}' is already registered.")
        
        SAVERS[saver_name] = saver_function

        # Register the extensions
        for extension in extensions:
            EXTENSION_MAPPING[extension] = saver_name

        return saver_function
    return decorator


@register_saver("pickle", ["pkl", "pickle"])
def save_pickle(data: Any, file_path: Path, **kwargs):
    """Save data using the pickle saver."""
    import pickle
    with open(file_path, "wb") as file:
        pickle.dump(data, file, **kwargs)

@register_saver("joblib", ["joblib"])
def save_joblib(data: Any, file_path: Path, **kwargs):
    """Save data using the joblib saver."""
    try:
        import joblib
    except ImportError:
        raise ImportError("joblib package is required for joblib saving. "
                          "Install it using `pip install joblib`.")
    joblib.dump(data, file_path, **kwargs)

@register_saver("hdf5", ["h5", "hdf5", "hdf"])
def save_hdf5(data: Any, file_path: Path, dataset_name: str = "dataset", **kwargs):
    """
    Save data using the HDF5 saver.

    Parameters
    ----------
    data : Any
        The data to save. Can be a dictionary of arrays or a single array.
    file_path : Path
        The path to the HDF5 file.
    dataset_name : str, optional
        The name of the dataset if `data` is not a dictionary. Default is "dataset".
    kwargs : dict
        Additional keyword arguments to pass to the h5py dataset creation.
    
    Raises
    ------
    ValueError
        If the data type is not supported.
    """
    try:
        import h5py
    except ImportError:
        raise ImportError("h5py package is required for HDF5 saving. "
                          "Install it using `pip install h5py`.")
    
    with h5py.File(file_path, "w") as file:
        if isinstance(data, dict):
            for key, value in data.items():
                file.create_dataset(key, data=value, **kwargs)
        else:
            file.create_dataset(dataset_name, data=data, **kwargs)

@register_saver("json", ["json"])
def save_json(data: Any, file_path: Path, **kwargs):
    """Save data using the json saver."""
    import json
    with open(file_path, "w") as file:
        json.dump(data, file, **kwargs)

@register_saver("str", ["txt", "html", "log", "md", "rst"])
def save_str(data, file_path: Path, **kwargs):
    """Save data using the txt saver."""
    with open(file_path, "w") as file:
        file.write(str(data), **kwargs)

@register_saver("numpy", ["npz", "npy"])
def save_numpy(data: Any, file_path: Path, **kwargs):
    """Save data using the numpy saver."""
    try:
        import numpy as np
    except ImportError:
        raise ImportError("numpy package is required for numpy saving. "
                          "Install it using `pip install numpy`.")
    
    # Check if data is a torch.Tensor by checking for 'cpu' and 'numpy' methods
    if hasattr(data, 'cpu') and hasattr(data, 'numpy'):
        data = data.cpu().numpy()

    # If data is not already a NumPy array, convert it
    if not isinstance(data, np.ndarray):
        data = np.array(data)

    ext = file_path.suffix.lstrip(".").lower()
    if ext == "npz":
        if not isinstance(data, dict):
            raise ValueError("NPZ saver expects data to be a dictionary of arrays.")
        np.savez(file_path, **data, **kwargs)
    elif ext == "npy":
        np.save(file_path, data, **kwargs)
    else:
        raise ValueError(f"Extension {ext} is not supported for numpy saving. "
                        f"Use one of {EXTENSION_MAPPING.keys()} or use directly the numpy saver.")

@register_saver("pandas", ["csv", "parquet", "xlsx", "xls", "feather"])
def save_pandas(data: Any, file_path: Path, **kwargs):
    """Save data using the pandas saver."""
    import pandas as pd

    data = pd.DataFrame(data)

    ext = file_path.suffix.lstrip(".").lower()
    if ext == "csv":
        data.to_csv(file_path, **kwargs)
    elif ext == "parquet":
        data.to_parquet(file_path, **kwargs)
    elif ext == "xlsx" or ext == "xls":
        data.to_excel(file_path, **kwargs)
    elif ext == "feather":
        data.to_feather(file_path, **kwargs)
    else:
        raise ValueError(f"Extension {ext} is not supported for pandas saving. "
                        f"Use one of {EXTENSION_MAPPING.keys()} or use directly the pandas saver.")

@register_saver("pillow", ["jpg", "jpeg", "png", "bmp", "gif", "tiff", "tif", "webp"])
def save_pillow(data: Any, file_path: Path, **kwargs):
    """Save data using the pillow saver."""
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("Pillow package is required for pillow saving. "
                          "Install it using `pip install pillow`.")
    if not isinstance(data, Image.Image):
        raise ValueError("Pillow saver expects data to be an instance of PIL.Image.")
    data.save(file_path, **kwargs)

@register_saver("pytorch", ["pt", "pth"])
def save_pytorch(data: Any, file_path: Path, **kwargs):
    """Save data using the pytorch saver."""
    try:
        import torch
    except ImportError:
        raise ImportError("torch package is required for pytorch saving. "
                          "Install it using `pip install torch`.")
    torch.save(data, file_path, **kwargs)

@register_saver("yaml", ["yaml", "yml"])
def save_yaml(data: Any, file_path: Path, **kwargs):
    """Save data using the YAML saver."""
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML is required to save .yaml files. "
                          "Install it using `pip install pyyaml`.")
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file, **kwargs)

@register_saver("ini", ["ini", "cfg"])
def save_ini(data: Any, file_path: Path, **kwargs):
    """Save data using the INI saver."""
    if not isinstance(data, dict):
        raise ValueError("INI saver expects data to be a dictionary.")
    import configparser    
    config = configparser.ConfigParser()
    for section, params in data.items():
        config[section] = params
    with open(file_path, "w") as file:
        config.write(file)

@register_saver("matlab", ["mat"])
def save_matlab(data: Any, file_path: Path, **kwargs):
    """Save data using the MATLAB saver."""
    if not isinstance(data, dict):
        raise ValueError("MATLAB saver expects data to be a dictionary.")
    try:
        import scipy.io
    except ImportError:
        raise ImportError("scipy.io is required to save .mat files. "
                          "Install it using `pip install scipy`.")
    
    scipy.io.savemat(file_path, data, **kwargs)

@register_saver("audio", ["wav", "mp3", "flac", "ogg"])
def save_audio(data: Any, file_path: Path, **kwargs):
    """Save data using the audio saver."""
    try:
        import soundfile as sf
    except ImportError:
        raise ImportError("soundfile is required to save audio files. "
                          "Install it using `pip install soundfile`.")
    sf.write(file_path, data, **kwargs)

@register_saver("video", ["mp4", "avi", "mov", "mkv"])
def save_video(data: Any, file_path: Path, **kwargs):
    """Save data using the video saver."""
    from ..video.video_writer import write_video
    write_video(file_path=file_path, frames=data, **kwargs)