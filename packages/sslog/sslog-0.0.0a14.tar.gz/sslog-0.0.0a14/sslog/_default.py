from os import environ
from typing import TypeVar


T = TypeVar("T")


def env(key: str, typ: type[T], default=None) -> T:
    if key not in environ:
        return default

    val = environ[key]

    if typ == str:
        return val
    if typ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    if typ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None
    raise ValueError("The requested type '%r' is not supported" % typ)


use_json: bool = env("SSLOG_JSON", bool, False)
