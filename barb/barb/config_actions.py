"""Parses configuration files & gets system / user environment variables.

Example usage:
``ConfigValues.load('path/to/file.yaml', include_environ_vars=True)``

Access variables by:
``print(ConfigValues.variable1)
  print(ConfigValues.FILE_SOURCE)``

If you get warning messages from the IDE saying Unresolved reference
for ConfigValues.variable can subclass the ConfigValues,
and add type hints to the variables.

class MyConfigValues(ConfigValues):
    variable1: str
    FILE_SOURCE: str

"""

import os
from typing import Optional, Union, Sequence, Callable, List, Dict, Any

import json
import yaml

from barb.constants import CONFIG_FILE_PATH


class ConfigValues:  # pylint: disable=too-few-public-methods
    """Loads the config variables from the file &
    loads the keys as class parameters.
    Access the config variables anywhere in your code by doing
    ConfigValues.VARIABLE_NAME (don't assign it to a variable name)
    """

    CYZ: str


    @classmethod
    def load(
        cls,
        config_path: Optional[str],
        output_validator: Optional[
            Union[Sequence[str], Callable[[Dict[str, Any]], None]]
        ] = None,
        include_environ_vars: Union[List[str], bool] = False,
        ext: Optional[str] = None,
    ) -> None:
        """Loads the config variables from the file & loads the
        keys as class parameters.
       :param: config_path: path/to/config_file.ext
       :param: output_validator:
                - if a function, it checks if the loaded config values
                  contain the correct keys, are of the correct type, values, etc.
                - if an iterable, checks all items in that iterable
                  are in the output dictionary
       :param: include_environ_vars:
                - if an iterable (i.e. list, tuple, ...) only includes the items
                  that are in that iterable.
                - if False, returns an empty dictionary
                - if True, includes all the environment variables
       :param: ext: File extension, only needs to be specified if the extension
                    of the filename does not match the parser format, e.g.
                    filename is ``abcdef.xyz``, but is an ``ini`` file.
        """
        cls._load_config_vars(
            config_path=config_path,
            output_validator=output_validator,
            include_environ_vars=include_environ_vars,
            ext=ext,
        )
        cls._load_config_vars_as_class_properties()

    @classmethod
    def _load_config_vars(
        cls,
        config_path: Optional[str],
        output_validator: Optional[
            Union[Sequence[str], Callable[[Dict[str, Any]], None]]
        ],
        include_environ_vars: Union[List[str], bool],
        ext: Optional[str] = None,
    ) -> None:
        """Loads the config_variables
        :param: config_path: path/to/config_file
                """
        cls.config_dict = load_config_vars(
            path=config_path,
            include_environ_vars=include_environ_vars,
            output_validator=output_validator,
            ext=ext,
        )

    @classmethod
    def _load_config_vars_as_class_properties(cls) -> None:
        """Loads the dictionary configuration file as the classes properties"""
        for key in cls.config_dict:
            setattr(cls, key, cls.config_dict[key])


def load_config_vars(
    path: Optional[str],
    output_validator: Optional[Union[Sequence[str], Callable[[Dict[str, Any]], None]]],
    include_environ_vars: Union[List[str], bool],
    ext: Optional[str] = None,
) -> Dict[str, Any]:
    """Loads the configuration variables. Loads the variables from the
    file (if a path is passed) and the environment variables.
       :param: path: path/to/config_file.ext
       :param: output_validator:
                - if a function, it checks if the loaded config values
                  contain the correct keys, are of the correct type, values, etc.
                - if an iterable, checks all items in that iterable
                  are in the output dictionary
       :param: include_environ_vars:
                - if an iterable (i.e. list, tuple, ...) only includes the items
                  that are in that iterable.
                - if False, returns an empty dictionary
                - if True, includes all the environment variables
       :param: ext: File extension, only needs to be specified if the extension
                    of the filename does not match the parser format, e.g.
                    filename is ``abcdef.xyz``, but is an ``ini`` file.
       :returns: Dictionary of {config_name: config_value}
       """

    env_vars = load_env_vars(include_environ_vars, None)
    config_dict = parse_config_file(path, ext) if path else dict()
    output_dict = {**env_vars, **config_dict}
    _validate_output(output_dict, output_validator, path)
    return output_dict


def load_env_vars(
    include_environ_vars: Union[Sequence[str], bool],
    output_validator: Optional[
        Union[Sequence[str], Callable[[Dict[str, Any]], None]]
    ] = None,
) -> Dict[str, str]:
    """
    :param: include_environ_vars:
                - if an iterable (i.e. list, tuple, ...) only returns the items
                  that are in that iterable.
                - if False, returns an empty dictionary
                - if True, loads all the environment variables
    :returns: The system's user & global environment variables."""

    output_dict: Dict[str, str]
    if not include_environ_vars:
        output_dict = dict()
    elif include_environ_vars is True:
        output_dict = dict(os.environ)
    else:
        output_dict = {
            k: v
            for k, v in os.environ.items()
            if k in include_environ_vars  # type: ignore  #bug 6113
        }
    _validate_output(output_dict, output_validator)
    return output_dict


def _validate_output(
    output_dict: Dict[str, Any],
    output_validator: Optional[Union[Sequence[str], Callable[[Dict[str, Any]], None]]],
    path: Optional[str] = None,
) -> None:
    """Checks if the output dictionary matches what is expected. Raises an error otherwise.
    :param: output_dict: The output dictionary of {config_variable: config_value}
    :param: output_validator: a list of keys to be expected in the dictionary OR a callable
                             function that tests the dictionary
    :param: path: 'C:/path/to/file.ext' - only needed for a clearer error message.
    :return: None
    """
    if output_validator is None:
        return

    if callable(output_validator):
        output_validator(output_dict)
        return

    missing_vars = [
        config_var for config_var in output_validator if config_var not in output_dict
    ]
    if missing_vars:
        # error msg will only include the path if the path is specified.
        path_str = "either the {path} or ".format(path=path) if path else ""
        missing_vars_str = ["'{var}'".format(var=var) for var in missing_vars]
        raise KeyError(
            "The config variables [{config_vars}] were "
            "not found in {path_str}"
            "the User or System Environment Variables. "
            "If you have recently set the environment variable, you "
            "must spawn a new process of the cmd prompt/terminal window "
            "for the changes to take effect.".format(
                config_vars=", ".join(missing_vars_str), path_str=path_str
            )
        )

    return


def _load_ini(path: str) -> Dict[str, str]:
    """Loads a .ini file & returns the dictionary
    Note - loses case sensitivity of the <key> in the key=value section
    :param: path: C:/path/to/file.yaml
    :returns: parsed yaml dictionary"""

    import configparser

    class IniParser(  # pylint: disable=too-many-ancestors
        configparser.ConfigParser, configparser.RawConfigParser
    ):
        """Adds function to the default ConfigParser."""

        def as_dict(self) -> Dict[str, str]:
            """Converts the output as dictionary."""
            ini_dict = dict(
                self._sections  # type: ignore  # doesn't recognise self._sections
            )
            for k in ini_dict:
                ini_dict[k] = dict(
                    self._defaults, **ini_dict[k]  # type: ignore  # no self._defaults
                )
                ini_dict[k].pop("__name__", None)
            return ini_dict

    config = IniParser()
    config.read(path)
    return config.as_dict()


def _load_py(path: str) -> Dict[str, Any]:
    """
    Loads a .py file & returns the variables
    :param: path: C:/path/to/file.yaml
    :return: dictionary of global variables in that python file
    """
    from runpy import run_path

    config: Dict[str, Any]

    config = run_path(path)
    config = {k: v for k, v in config.items() if not k.startswith("__")}
    return config


def load_json(path: str) -> Dict[str, Any]:
    """
    Loads a .json file & returns the variables
    :param path: C:/path/to/file.yaml
    :return: dictionary of global variables in that python file
    """
    with open(path) as file:
        config = json.loads(file.read())
    return config


def parse_config_file(path: str, ext: Optional[str] = None) -> Dict[str, Any]:
    """
    :param: path: path/to/config_file.ext
    :param: ext: File extension, only needs to be specified if the extension
                    of the filename does not match the parser format, e.g.
                    filename is ``abcdef.xyz``, but is an ``ini`` file.
    :return: the parsed config file dictionary
    """

    extension_parser_dict = {
        ".ini": _load_ini,
        ".yaml": _load_yaml,
        ".yml": _load_yaml,
        ".py": _load_py,
        ".json": load_json,
    }
    _, extension = os.path.splitext(path)
    extension = extension if ext is None else ext
    try:
        parser = extension_parser_dict[extension]
    except KeyError:
        raise NotImplementedError(
            "No matching parser found "
            + "for '{extension}', when trying to parse ".format(extension=extension)
            + "{path}. ".format(path=path)
            + "Available extensions to parse are:"
            + " [{}]".format(", ".join(extension_parser_dict.keys()))
        )
    config_dict = parser(path)
    return config_dict


def _load_yaml(path: str) -> Dict[str, Any]:
    """Loads a yaml file & returns the dictionary
    :param: path: C:/path/to/file.yaml
    :returns: parsed yaml dictionary"""

    out_dict: Dict[str, Any]

    with open(path) as f:
        out_dict = yaml.load(f, Loader=yaml.FullLoader)
    return out_dict




def load_config(file_path: str = CONFIG_FILE_PATH) -> None:
    """ Loads the config file, and the dependant config file in
    PLATFORM_KEY_COLUMNS_CONFIG_PATH.
    Tries to load the path itself, then tries to load it in the same path
    as where the other config file exists, otherwise raises a FileNotFound Error.
    :param file_path: path to the config file.
    """
    ConfigValues.load(file_path)
