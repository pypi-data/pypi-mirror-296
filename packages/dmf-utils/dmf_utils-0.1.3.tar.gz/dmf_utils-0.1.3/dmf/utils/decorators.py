
from typing import Callable, List, Union

def copy_docstring(from_func):
    """
    Decorator to copy the docstring from one function to another.

    Parameters
    ----------
    from_func : function
        The function from which the docstring should be copied.

    Returns
    -------
    function
        The decorated function with the copied docstring.
    """
    def decorator(to_func: Callable):
        to_func.__doc__ = from_func.__doc__
        return to_func
    return decorator


def register(dictionary: dict, keys: Union[str, List[str]]):
    """
    Decorator to register a function in a dictionary.
    Used to register functions in different modules.

    Parameters
    ----------
    dictionary : dict
        The dictionary where the function will be registered.
    keys : List[str]
        The list of keys that the function
    """
    if isinstance(keys, str):
        keys = [keys]
        
    def decorator(func: Callable):
        for key in keys:
            dictionary[key] = func
        return func

    return decorator