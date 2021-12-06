import importlib
from uvicorn.workers import UvicornWorker


class DynamicUvicornWorker(UvicornWorker):
    """
    This class is called `DynamicUvicornWorker` because it assigns values
    according to the module available Union['asyncio', 'uvloop']
    It also set `lifespan` to `off` :)
    """

    spam_spec = importlib.util.find_spec("uvloop")
    found = spam_spec is not None
    if found:
        CONFIG_KWARGS = {"loop": "uvloop", "http": "auto", "lifespan": "off"}
    else:
        CONFIG_KWARGS = {"loop": "auto", "http": "auto", "lifespan": "off"}