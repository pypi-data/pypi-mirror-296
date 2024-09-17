from pathlib import Path
from typing import Optional, Union, Callable

from ..utils.decorators import register


DECOMPRESSORS = {}

def decompress(
    input_file: Union[str, Path],
    output_dir: Union[str, Path] = "./",
    compression: Optional[str] = None,
    password: Optional[str] = None,
    **kwargs,
) -> Path:
    """
    Decompress a compressed file.

    This function decompresses a file based on its extension or the specified compression format.
    Supported formats include gzip, bzip2, xz, zip, 7z, and various tar-based formats.

    Supported Formats
    -----------------
    - gzip (.gz, .gzip)
    - bzip2 (.bz2, .bzip2)
    - xz (.xz)
    - zip (.zip)
    - 7z (.7z)
    - tar (.tar)
    - tar.gz (.tar.gz, .tgz)
    - tar.bz2 (.tar.bz2)
    - tar.xz (.tar.xz)

    Parameters
    ----------
    input_file : Union[str, Path]
        The compressed input file path.
    output_dir : Union[str, Path], optional
        The directory where files should be extracted. Defaults to the current directory ("./").
    compression : Optional[str], optional
        The compression format. If not provided, it will be inferred from the file extension.
    password : Optional[str], optional
        Password for the archive, supported only for ZIP and 7z formats.
    kwargs : dict
        Additional keyword arguments to pass to the decompression function.

    Returns
    -------
    Path
        The path to the directory containing the decompressed files.

    Raises
    ------
    ValueError
        If the input file is invalid or if the compression format is unsupported.
    NotImplementedError
        If password protection is used with an unsupported compression format.
    ImportError
        If a required library for a specific compression format is not installed.

    Examples
    --------
    Example 1: Decompressing a gzip file

    .. code-block:: python

        decompress("example.gz", output_dir="output")

    Example 2: Decompressing a zip file

    .. code-block:: python

        decompress("example.zip", output_dir="output")

    Example 3: Decompressing a 7z file with a password

    .. code-block:: python

        decompress("example.7z", output_dir="output", password="mypassword")

    Notes
    -----
    - The function automatically detects the compression format based on the file extension.
    - The output directory will be created if it does not exist.
    - For unsupported formats or missing libraries, appropriate errors are raised.
    """
    input_file = Path(input_file)
    output_dir = Path(output_dir)

    if not input_file.exists() or not input_file.is_file():
        raise ValueError(
            f"Input file does not exist or is not a valid file: {input_file}"
        )
    
    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)

    if not compression:
        for key in DECOMPRESSORS.keys():
            if input_file.name.endswith("." + key):
                compression = key
                break
    
    compression = compression.lower().lstrip(".")
    decompressor_func = DECOMPRESSORS.get(compression)
    if not decompressor_func:
        raise ValueError(
            f"Compression format {compression} is not supported. Use one of {list(DECOMPRESSORS.keys())}."
        )
    
    decompressor_func(input_file, output_dir, password=password, **kwargs)
    
    return output_dir

@register(DECOMPRESSORS, ["gz", "gzip"])
def decompress_gzip(
    input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Decompress a gzip file."""
    import gzip
    _check_password_none(password)
    _generic_decompresor(input_file, output_dir, gzip.open, **kwargs)


@register(DECOMPRESSORS, ["bz2", "bzip2"])
def decompress_bzip2(
    input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Decompress a bzip2 file."""
    import bz2
    _check_password_none(password)
    _generic_decompresor(input_file, output_dir, bz2.open, **kwargs)


@register(DECOMPRESSORS, "xz")
def decompress_xz(
    input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Decompress an xz file."""
    import lzma
    _check_password_none(password)
    _generic_decompresor(input_file, output_dir, lzma.open, **kwargs)


@register(DECOMPRESSORS, "zip")
def decompress_zip(
    input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Decompress a zip file."""
    import zipfile

    with zipfile.ZipFile(input_file, "r") as zipf:
        if password:
            zipf.setpassword(password.encode())
        zipf.extractall(output_dir)


@register(DECOMPRESSORS, "7z")
def decompress_7z(
    input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Decompress a 7z file."""
    try:
        import py7zr
    except ImportError:
        raise ImportError(
            "py7zr package is required for 7z decompression. Install it using `pip install py7zr`."
        )

    with py7zr.SevenZipFile(input_file, "r", password=password, **kwargs) as archive:
        archive.extractall(output_dir)


@register(DECOMPRESSORS, ["tgz", "tar.gz", "tar.bz2", "tar.xz", "tar"])
def decompress_tar(
    input_file: Path, output_dir: Path, password: Optional[str] = None, **kwargs
) -> None:
    """Decompress a tar file."""
    import tarfile

    _check_password_none(password)

    with tarfile.open(input_file, "r") as tar:
        tar.extractall(output_dir)

def _check_password_none(password: Optional[str]) -> None:
    """Check if the password is None."""
    if password:
        raise NotImplementedError(
            f"Password protection is not supported for this format. "
            "Use for example ZIP or 7z formats."
        )

def _generic_decompresor(
    input_file: Path,
    output_dir: Path,
    decompressor: Callable,
    **kwargs,
) -> None:
    """Generic decompressor function."""
    import shutil

    with decompressor(input_file, "rb", **kwargs) as f_in, open(
        output_dir / input_file.stem, "wb"
    ) as f_out:
        shutil.copyfileobj(f_in, f_out)