
from pathlib import Path
from typing import Optional, Union, Callable

from ..utils.decorators import register

COMPRESSORS = {}

def compress(
    input_file: Union[str, Path],
    compression: Optional[str] = None,
    output_file: Optional[Union[str, Path]] = None,
    password: Optional[str] = None,
    **kwargs,
) -> Path:
    """
    Compress a file or directory into a specified format.

    This function compresses a file or directory using various compression formats such as gzip, bzip2, xz, zip, 7z, and tar-based formats. The format can either be specified directly or inferred from the output file extension.

    Parameters
    ----------
    input_file : Union[str, Path]
        The path to the input file or directory to be compressed.
    compression : Optional[str], default=None
        The compression format to use. If not provided, it will be inferred from the output file extension or defaults to "zip".
    output_file : Optional[Union[str, Path]], default=None
        The path for the output compressed file. If not provided, it will be derived from the input file path by appending the appropriate file extension.
    password : Optional[str], default=None
        Password for the archive, supported only for ZIP and 7z formats.
    kwargs : dict
        Additional keyword arguments to pass to the compression function.

    Returns
    -------
    Path
        The path to the compressed output file.

    Raises
    ------
    FileExistsError
        If the input file does not exist.
    ValueError
        If both `compression` and `output_file` are provided, or if the compression format is unsupported.
    NotImplementedError
        If password protection is specified for a format that does not support it.

    Notes
    -----
    Either `compression` or `output_file` must be provided, but not both. If neither is provided, the default compression format "zip" is used.

    - If `output_file` is provided without a specified `compression`, the format will be inferred from the file extension.
    - If `compression` is provided without an `output_file`, the output file path is derived by appending the appropriate file extension to the `input_file` path.
    - Password protection is only supported for ZIP and 7z formats.

    Examples
    --------
    Compressing a directory into a zip file

    .. code-block:: python

        compress("my_folder", compression="zip")

    Compressing a file into a gzip file

    .. code-block:: python

        compress("data.txt", output_file="data.txt.gz")

    Compressing a directory with a specified output file and inferred format

    .. code-block:: python

        compress("my_folder", output_file="my_folder.tar.gz")

    Compressing a directory into a password-protected file

    .. code-block:: python

        compress("my_folder", compression="7z", password="mypassword")
    """

    input_file = Path(input_file)
    if not input_file.exists():
        raise FileExistsError(f"Input file {input_file} does not exist.")

    # Check that compression or output_file is provided. Only one.
    if compression and output_file:
        raise ValueError("Only one of compression or output_file must be provided.")

    if output_file:
        output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        compression = next(
            (ext for ext in COMPRESSORS if output_file.name.endswith(f".{ext}")),
            None,
        )
    if not output_file:
        compression = compression or "zip"
        compression = compression.lower().lstrip(".")
        output_file = input_file.with_suffix(input_file.suffix + f".{compression}")

    compressor_func = COMPRESSORS.get(compression)
    if not compressor_func:
        raise ValueError(
            f"Compression format {compression} is not supported. "
            f"Use one of {list(COMPRESSORS.keys())}."
        )

    compressor_func(input_file, output_file, password=password, **kwargs)

    return output_file


@register(COMPRESSORS, ["gz", "gzip"])
def compress_gzip(
    input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Compress a file using gzip."""
    import gzip

    _check_no_folder(input_file)
    _check_password_none(password)
    _generic_compressor(input_file, output_file, gzip.open, **kwargs)


@register(COMPRESSORS, ["bz2", "bzip2"])
def compress_bzip2(
    input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Compress a file using bzip2."""
    import bz2

    _check_no_folder(input_file)
    _check_password_none(password)
    _generic_compressor(input_file, output_file, bz2.open, **kwargs)


@register(COMPRESSORS, ["xz"])
def compress_xz(
    input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Compress a file using xz."""
    import lzma

    _check_no_folder(input_file)
    _check_password_none(password)
    _generic_compressor(input_file, output_file, lzma.open, **kwargs)


@register(COMPRESSORS, ["zip"])
def compress_zip(
    input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Compress a file or directory using zip."""
    import os
    import zipfile

    # To support password protection we would need to use library like pyzipper
    _check_password_none(password)
    
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED, **kwargs) as zipf:
        if input_file.is_dir():
            root_folder_name = input_file.name  # Get the name of the directory
            for root, _, files in os.walk(input_file):
                for file in files:
                    # Add the root folder name to the path within the zip
                    zipf.write(
                        Path(root) / file, 
                        Path(root_folder_name) / Path(root).relative_to(input_file) / file
                    )
        else:
            zipf.write(input_file, input_file.name)


@register(COMPRESSORS, ["7z"])
def compress_7z(
    input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Compress a file or directory using 7z."""
    try:
        import py7zr
    except ImportError:
        raise ImportError(
            "py7zr package is required for 7z compression. "
            "Install it using `pip install py7zr`."
        )

    with py7zr.SevenZipFile(output_file, "w", password=password, **kwargs) as archive:
        if input_file.is_dir():
            archive.writeall(input_file, arcname=input_file.name)
        else:
            archive.write(input_file, arcname=input_file.name)


@register(COMPRESSORS, ["tar", "tgz", "tar.gz", "tar.bz2", "tar.xz"])
def compress_tar(
    input_file: Path, output_file: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Compress a file or directory using tar."""
    import tarfile

    _check_password_none(password)

    mode_mapping = {
        "tgz": "w:gz",
        "tar.gz": "w:gz",
        "tar.bz2": "w:bz2",
        "tar.xz": "w:xz",
        "tar": "w",
    }

    # Compression is first match that ends with the input file suffix
    compression = next(
        (comp for comp in mode_mapping if input_file.suffix.endswith(comp)), "tar"
    )
    if input_file.is_dir() or input_file.is_file():
        with tarfile.open(output_file, mode_mapping[compression], **kwargs) as tar:
            tar.add(input_file, arcname=input_file.name)
    else:
        raise ValueError("Invalid input for tar compression.")


def _generic_compressor(
    input_file: Path,
    output_file: Path,
    compressor: Callable,
    **kwargs,
) -> None:
    """Generic compressor function."""
    import shutil

    with open(input_file, "rb") as f_in, compressor(
        output_file, "wb", **kwargs
    ) as f_out:
        shutil.copyfileobj(f_in, f_out)


def _check_password_none(password: Optional[str]) -> None:
    """Check if password is None."""
    if password:
        raise NotImplementedError(
            "Password protection is not supported for the compression format. "
            "Supported only for ZIP and 7z formats."
        )


def _check_no_folder(input_file: Path) -> None:
    """Check if the input file is a folder."""
    if input_file.is_dir():
        raise ValueError(
            "Compressing folders is not supported. "
            "Use tar format instead, zip or 7z for exampel."
        )
