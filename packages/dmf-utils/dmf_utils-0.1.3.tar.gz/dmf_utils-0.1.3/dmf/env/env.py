from pathlib import Path
from typing import Optional, Union, Dict
import os
from dotenv import load_dotenv, set_key, unset_key, dotenv_values

from ..utils.decorators import copy_docstring
from ..utils.typing import Literal

__all__ = ["EnvManager", "env", "setup", "getenv", "setenv", "unsetenv"]


class EnvManager:
    """
    A manager for handling environment variables across different levels, including user, project, and system.

    The `EnvManager` class simplifies the management of environment variables by allowing you to load,
    set, unset, and retrieve variables from different sources such as user-level `.env` files,
    project-level `.env` files, or directly from the system's environment variables.

    Examples
    --------
    Basic Usage:
    >>> env = EnvManager().setup()
    >>> env.setenv('API_KEY', '12345', environ='project')
    >>> print(env.getenv('API_KEY'))
    '12345'
    >>> del env['API_KEY']

    Chained Setup:
    >>> env = EnvManager().setup(project_env_path="my_project.env", user_env_path="~/.custom_env", override=True)
    >>> env.setenv('SECRET_KEY', 'abcdef', environ='user')

    Using Global Instance:
    >>> from dmf.env import env, getenv, setenv, unsetenv
    >>> setenv('DATABASE_URL', 'sqlite:///mydb.db', environ='project')
    >>> print(getenv('DATABASE_URL'))
    'sqlite:///mydb.db'
    >>> unsetenv('DATABASE_URL')
    """

    def __init__(self):
        self._is_initialized = False
        self._project_env_path: Optional[Path] = None
        self._user_env_path: Optional[Path] = None
        self._override = False

    def setup(
        self,
        project_env_path: Union[str, Path] = ".env",
        user_env_path: Union[str, Path] = "~/.env.dmf",
        override: bool = False,
    ) -> "EnvManager":
        """
        Set up the environment by loading variables from user and project `.env` files.

        Parameters
        ----------
        project_env_path : Union[str, Path], optional
            The path to the project's `.env` file. Defaults to ".env".
        user_env_path : Union[str, Path], optional
            The path to the user's `.env.dmf` file. Defaults to "~/.env.dmf".
        override : bool, optional
            Whether to override existing environment variables with values from the `.env` files. Defaults to False.

        Returns
        -------
        EnvManager
            The initialized `EnvManager` instance.
        """
        self._project_env_path = Path(project_env_path)
        self._user_env_path = Path(user_env_path).expanduser()
        self._override = override

        if self._user_env_path.exists():
            load_dotenv(self._user_env_path, override=self._override)

        if self._project_env_path.exists():
            load_dotenv(self._project_env_path, override=self._override)

        self._is_initialized = True
        return self

    def _ensure_setup(self):
        if not self._is_initialized:
            self.setup()

    def getenv(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieve an environment variable's value.

        Parameters
        ----------
        key : str
            The name of the environment variable.
        default : Optional[str], optional
            The default value to return if the environment variable is not found. Defaults to None.

        Returns
        -------
        Optional[str]
            The value of the environment variable, or the default value if the variable is not set.
        """
        self._ensure_setup()
        return os.getenv(key, default)

    # Alias the `getenv` method to `get` for easier access
    get = getenv

    def setenv(
        self, key: str, value: str, scope: Optional[Literal["project", "user"]] = None
    ):
        """
        Set an environment variable.

        Parameters
        ----------
        key : str
            The name of the environment variable.
        value : str
            The value to set for the environment variable.
        scope : Optional[Literal["project", "user"]], optional
            The environment in which to set the variable. Can be "project" or "user". Defaults to None.
        """
        self._ensure_setup()
        os.environ[key] = value

        if scope == "project":
            if not self._project_env_path.exists():
                self._project_env_path.touch()
            set_key(str(self._project_env_path), key, value)
        elif scope == "user":
            if not self._user_env_path.exists():
                self._user_env_path.touch()
            set_key(str(self._user_env_path), key, value)

    def unsetenv(self, key: str, scope: Optional[Literal["project", "user"]] = None):
        """
        Unset (delete) an environment variable.

        Parameters
        ----------
        key : str
            The name of the environment variable to unset.
        scope : Optional[Literal["project", "user"]], optional
            The environment from which to unset the variable. Can be "project" or "user". Defaults to None.
        """
        self._ensure_setup()
        os.environ.pop(key, None)

        if (
            scope == "project"
            and self._project_env_path
            and self._project_env_path.exists()
        ):
            unset_key(str(self._project_env_path), key)
        elif scope == "user" and self._user_env_path.exists():
            unset_key(str(self._user_env_path), key)

    def __getitem__(self, key: str) -> str:
        """Retrieve an environment variable using dictionary-like access."""
        self._ensure_setup()
        return os.environ[key]

    def __setitem__(self, key: str, value: str):
        """Set an environment variable using dictionary-like access."""
        self.setenv(key, value)

    def __delitem__(self, key: str):
        """Delete an environment variable using dictionary-like access."""
        self.unsetenv(key)

    def __repr__(self) -> str:
        """Return a string representation of the `EnvManager` instance."""
        return f'<EnvManager project="{self._project_env_path}" user="{self._user_env_path}">'

    def load(self, env_file: Union[str, Path]) -> None:
        """
        Load environment variables from a specified file.

        Parameters
        ----------
        env_file : Union[str, Path]
            The path to the `.env` file to load.
        """
        self._ensure_setup()
        load_dotenv(dotenv_path=env_file, override=self._override)

    def load_from_str(self, dotenv_string: str) -> None:
        """
        Load environment variables from a string.

        Parameters
        ----------
        dotenv_string : str
            A string containing environment variable definitions.
        """
        self._ensure_setup()
        env_vars = dotenv_values(stream=dotenv_string)
        for key, value in env_vars.items():
            os.environ[key] = value

    def all(self, scope: Optional[Literal['project', 'user']] = None, pattern: Optional[str] = None) -> Dict[str, str]:
        """
        Retrieve all environment variables, optionally filtered by a pattern.

        Parameters
        ----------
        scope : Optional[Literal['project', 'user']], optional
            The scope of environment variables to retrieve. If 'project', returns variables from the project .env file. 
            If 'user', returns variables from the user .env file. If None, returns all variables from the current environment.
        pattern : Optional[str], optional
            A regex pattern to filter the environment variables by key name. Defaults to None, which means no filtering.

        Returns
        -------
        Dict[str, str]
            A dictionary containing all environment variables in the specified scope, filtered by the pattern if provided.

        Raises
        ------
        ValueError
            If an invalid scope is provided.
        """
        self._ensure_setup()
        
        if scope is None:
            env_vars = dict(os.environ)
        elif scope == 'project' and self._project_env_path.exists():
            env_vars = dict(dotenv_values(dotenv_path=self._project_env_path))
        elif scope == 'user' and self._user_env_path.exists():
            env_vars = dict(dotenv_values(dotenv_path=self._user_env_path))
        else:
            env_vars = {}

        if pattern:
            import re
            regex = re.compile(pattern)
            env_vars = {k: v for k, v in env_vars.items() if regex.search(k)}

        return env_vars


# Initialize the global instance of EnvManager
env = EnvManager()

# Alias the methods of the global instance for easier access
@copy_docstring(EnvManager.setup)
def setup(
    project_env_path: Union[str, Path] = ".env",
    user_env_path: Union[str, Path] = "~/.env.dmf",
    override: bool = False,
) -> EnvManager:
    return env.setup(project_env_path, user_env_path, override)


@copy_docstring(EnvManager.get)
def getenv(key: str, default: Optional[str] = None) -> Optional[str]:
    return env.get(key, default)


@copy_docstring(EnvManager.setenv)
def setenv(key: str, value: str, scope: Optional[Literal["project", "user"]] = None):
    env.setenv(key, value, scope)


@copy_docstring(EnvManager.unsetenv)
def unsetenv(key: str, scope: Optional[Literal["project", "user"]] = None):
    env.unsetenv(key, scope)
