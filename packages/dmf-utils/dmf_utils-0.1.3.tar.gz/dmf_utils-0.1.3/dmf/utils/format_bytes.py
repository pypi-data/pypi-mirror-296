

from typing import Optional

def bytes_to_human_readable(num_bytes: Optional[int], decimal_places: int = 2, units = ["Bytes", "KB", "MB", "GB", "TB"]) -> str:
    """
    Convert a number in bytes into a human-readable string with appropriate units (KB, MB, GB, TB).
    If num_bytes is None, return None.

    Parameters
    ----------
    num_bytes : int
        The number of bytes to convert. Can be a positive or negative integer.
    decimal_places : int, optional
        The number of decimal places to display for KB, MB, GB, and TB. Default is 2.

    Returns
    -------
    str or None
        The human-readable string representing the size in appropriate units, or None if input is None.
    """
    if num_bytes is None:
        return None

    # Define the units and thresholds (limited to TB)
    
    factor = 1024.0
    size = abs(num_bytes)
    unit_index = 0

    while size >= factor and unit_index < len(units) - 1:
        size /= factor
        unit_index += 1

    # Format the size based on the unit
    if units[unit_index] == "Bytes":
        size_str = f"{int(size)} {units[unit_index]}"
    else:
        size_str = f"{size:.{decimal_places}f} {units[unit_index]}"

    # Add a minus sign for negative byte values
    if num_bytes < 0:
        size_str = f"-{size_str}"

    return size_str