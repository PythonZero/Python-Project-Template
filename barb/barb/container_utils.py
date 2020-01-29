from typing import Dict, Any


def value_or_raise(dictionary: Dict[str, Any], key: str, error_msg: str) -> Any:
    """ Raise a keyError with a descriptive message if missing. Use {key}
    if the literal key needs to be part of the error message.
    :param dictionary: the dictionary
    :param key: the key
    :param error_msg: the error message
    :return: the key
    """
    try:
        return dictionary[key]
    except KeyError:
        raise KeyError(error_msg.format(key=key))
