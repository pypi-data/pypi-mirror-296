
try: # Compatibility with Python 3.7
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

__all__ = ["Literal"]