from __future__ import annotations
import json
import os
import pickle
import sys
from functools import partial
from loguru import logger as _logger
from glob import glob
from typing import *

__version__ = "0.0.1"

__all__ = [
    "logger", "load_text", "dump_text", "load_json", "dump_json", "load_pickle", "dump_pickle", "PathBuilder",
    "get_ext", "get_parent", "get_filename", "get_basename", "tuplify", "listify", "flatten", "AttrDict", "attrify"
]

PathLike = Union[str, os.PathLike]

def log(message: Any, *messages: Any, level: str, sep: str = " ", **kwargs: Any) -> None:
    getattr(_logger, level)(sep.join((repr(message), *(repr(m) for m in messages))), **kwargs)

class logger:
    """Helper class for convenience to record log with loguru.

    Using cases:
        >>> from datetime import datetime
        >>> logger.add(f"training-{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.log")
        >>> loss = ...
        >>> logger.info("train loss", loss.item())

        Here, the syntax is very similar to `print`, where you can send multiple inputs which later will be output. And
        the input can be any type, finally all inputs will automatically be converted to strings. Moreover, we also define
        aliases for the methods that exist in `loguru.logger` for the class. You can access these methods as you would
        in `loguru.logger`.
    """

    add = _logger.add
    bind = _logger.bind
    catch = _logger.catch
    complete = _logger.complete
    configure = _logger.configure
    contextualize = _logger.contextualize
    disable = _logger.disable
    enable = _logger.enable
    level = _logger.level
    log = _logger.log
    opt = _logger.opt
    parse = _logger.parse
    patch = _logger.patch
    remove = _logger.remove
    start = _logger.start
    stop = _logger.stop

    critical = partial(log, level="critical")
    debug = partial(log, level="debug")
    info = partial(log, level="info")
    warning = partial(log, level="warning")
    error = partial(log, level="error")
    exception = partial(log, level="exception")
    success = partial(log, level="success")
    trace = partial(log, level="trace")

def load_text(pathname: PathLike, mode: str = "r", encoding: str = None, **kwargs: Any) -> AnyStr:
    with open(pathname, mode, encoding=encoding or sys.getdefaultencoding(), **kwargs) as fp:
        return fp.read()

def dump_text(text: AnyStr, pathname: PathLike, mode: str = "w", encoding: str = None, **kwargs: Any) -> None:
    with open(pathname, mode, encoding=encoding or sys.getdefaultencoding(), **kwargs) as fp:
        fp.write(text)

def load_json(pathname: PathLike, loader: Optional[Callable] = None, **kwargs: Any) -> Any:
    with open(pathname, "r", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        return (loader or json.load)(fp, **kwargs)

def dump_json(obj: Any, pathname: PathLike, dumper: Optional[Callable] = None, **kwargs: Any) -> None:
    with open(pathname, "w", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        return (dumper or json.dump)(obj, fp, **kwargs)

def load_pickle(pathname: PathLike, **kwargs: Any) -> Any:
    with open(pathname, "rb") as fp:
        return pickle.load(fp, **kwargs)

def dump_pickle(obj: Any, pathname: PathLike, **kwargs: Any) -> None:
    with open(pathname, "wb") as fp:
        return pickle.dump(obj, fp, **kwargs)

class PathBuilder(os.PathLike):
    """Helper class to build paths.

    Using cases:
        >>> root = PathBuilder("log", "unet", mkdir=True)
        >>> checkpoints: PathBuilder = root / "checkpoints"
        >>> last_ckpt: str = checkpoints + "last.ckpt"

        As shown above, if the path root "log/unet" is not exists, PathBuilder will automatically create it when mkdir
        was set True. After that you can continue to build new paths via `/`, e.g. "log/unet/checkpoints", and final
        pathnames by `+`, e.g. "log/unet/checkpoints/last.ckpt".
    """

    def __init__(self, *names: str, mkdir: bool = True) -> None:
        self.mkdir = mkdir
        self._pathname = str(os.path.join(*(names or (".",))))
        os.makedirs(self._pathname, exist_ok=True) if mkdir else None

    @property
    def pathname(self) -> str:
        return self._pathname

    def parent(self) -> PathBuilder:
        return PathBuilder(os.path.dirname(self._pathname), mkdir=self.mkdir)

    def glob(self, pattern: str, **kwargs: Any) -> List[str]:
        return glob(os.path.join(self._pathname, pattern), **kwargs)

    def is_empty(self) -> bool:
        return len(os.listdir(self._pathname)) == 0

    def mkdir(self) -> None:
        os.makedirs(self._pathname, exist_ok=True)

    def join(self, *pathnames: str) -> PathBuilder:
        return PathBuilder(self._pathname, *pathnames, mkdir=self.mkdir)

    def __truediv__(self, name: str) -> PathBuilder:
        return PathBuilder(os.path.join(self._pathname, name), mkdir=self.mkdir)

    def __add__(self, name: str) -> str:
        return os.path.join(self._pathname, name)

    def __repr__(self) -> str:
        return self._pathname

    def __fspath__(self) -> str:
        return self._pathname

def get_ext(pathname: PathLike) -> str:
    return os.path.splitext(pathname)[1]

def get_parent(pathname: PathLike) -> str:
    return os.path.dirname(os.path.abspath(pathname))

def get_filename(pathname: PathLike) -> str:
    return os.path.splitext(os.path.basename(pathname))[0]

def get_basename(pathname: PathLike) -> str:
    return os.path.basename(pathname)

def tuplify(obj: Any) -> Tuple[Any]:
    """Coverts an object into a tuple object. The rules of conversion are as follows:
        a) if the `obj` is an iterable except str, each element of it will be pushed into a new tuple;
        b) if the `obj` is a type other than a, e.g. str, it will be wrapped with tuple.
    """
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return tuple(obj)
    return (obj,)

def listify(obj: Any) -> List[Any]:
    """Coverts an object into a list object. The rules of conversion are as follows:
        a) if the `obj` is an iterable except str, each element of it will be pushed into a new list;
        b) if the `obj` is a type other than a, e.g. str, it will be wrapped with list.
    """
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return list(obj)
    return [obj, ]

def flatten(seq: Iterable[Any]) -> Sequence[Any]:
    """Flattens a multiple nested iterable into a single nested sequence.

    Using cases:
        >>> flatten([1, 2, 3, [4, 5, 6, [7, 8, 9]]])
        >>> [1, 2, 3, 4, 5, 6, 7, 8, 9]

        Here a triple nesting sequence will be flattened into a single nested sequence.
    """
    for e in seq:
        if isinstance(e, Iterable) and not isinstance(e, (str, bytes)):
            yield from flatten(e)
        else:
            yield e

class AttrDict(Dict[str, Any]):
    """Attribute dictionary, allowing access to dict values as if they were class attributes.

    Using cases:
        >>> d = AttrDict({"name": "unet", "cfg": {"in_channels": 3, "num_classes": 9}})
        >>> d.cfg.num_classes
        9
        >>> d["cfg.decoder.depths"] = [2, 2, 2, 2]
        >>> d["cfg.decoder.depths"][0]
        2

        As shown above, you first need to covert an existing dict into AttrDict, and then you can access its value as
        you access a class/instance's properties. Moreover, you can get/set the value in `[]` via cascaded strings.
    """
    def __init__(self, d: Optional[Dict | Iterable] = None, **kwargs: Any) -> None:
        super(AttrDict, self).__init__()
        self.update(d, **kwargs)

    def update(self, d: Optional[Dict | Iterable] = None, **kwargs: Any) -> None:
        for k, v in dict(d or {}, **kwargs).items():
            self.__setattr__(k, v)

    def pop(self, k: str, default: Any = None) -> Any:
        delattr(self, k)
        return super(AttrDict, self).pop(k, default)

    def __setattr__(self, k: str, v: Any) -> None:
        def _covert_recursively(obj: Any) -> Any:
            if isinstance(obj, dict) and not isinstance(obj, AttrDict):
                return self.__class__(obj)
            if isinstance(obj, (tuple, list, set)):
                return type(obj)((_covert_recursively(e) for e in obj))
            return obj

        v = _covert_recursively(v)
        super(AttrDict, self).__setattr__(k, v)
        super(AttrDict, self).__setitem__(k, v)

    def __getattr__(self, k: str) -> Any:
        return super(AttrDict, self).__getitem__(k)

    def __setitem__(self, k: str, v: Any) -> None:
        if "." in k:
            k, suffix = k.split(sep=".", maxsplit=1)
            self.__setattr__(k, v={}) if k not in self else None
            self.__getattr__(k).__setitem__(suffix, v)
        else:
            self.__setattr__(k, v)

    def __getitem__(self, k: str) -> Any:
        if "." in k:
            prefix, k = k.rsplit(sep=".", maxsplit=1)
            return self.__getitem__(prefix)[k]
        return self.__getattr__(k)

def attrify(d: Optional[Dict | Iterable] = None, **kwargs: Any) -> AttrDict:
    return AttrDict(d, **kwargs)
