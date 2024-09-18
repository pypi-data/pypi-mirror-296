from __future__ import annotations
import json
import os
import pickle
import sys
from functools import partial, wraps
from loguru import logger as _logger
from glob import glob
from typing import *
from types import FunctionType

__version__ = "0.0.2"

__all__ = ["export", "logger", "PathBuilder", "AttrDict"]

PathLike = Union[str, os.PathLike]

def export(func: Optional[FunctionType] = None) -> Callable[..., Any]:
    """Export a function into its __all__."""
    @wraps(func)
    def _wrapper(func: FunctionType) -> Callable[..., Any]:
        return export(func)

    if func is None:
        return _wrapper

    func_name = func.__name__
    m = sys.modules[func.__module__]
    if hasattr(m, "__all__"):
        if func_name not in m.__all__:
            m.__all__.append(func_name)
    else:
        m.__all__ = [func_name]

    return func

@export
def prettify(obj: Any, encoder: Optional[Type[json.JSONEncoder]] = None, **kwargs: Any) -> str:
    """Prettify a Python object into an easy-to-read string. Due to its backed by json serializer, if an object cannot
    be serialized, a plain string of the object will be returned. Or you can opt to implement a special json encoder to
    serialize the object and to set it to the `encoder` argument when calling `prettify`.

    Using cases:
        >>> import albumentations as T
        >>> class MyJsonEncoder(json.JSONEncoder):
        >>>     def default(self, obj: Any) -> Any:
        >>>         if isinstance(obj, (T.BaseCompose, T.BaseCompose)):
        >>>             return r(8) if (r := getattr(obj, "indented_repr", None)) else repr(obj)
        >>>         return super(MyJsonEncoder, self).default(obj)
        >>> transform = T.Compose([T.Resize(224, 224), T.Normalize()])
        >>> prettify(transform, encoder=MyJsonEncoder)
        Compose([
          Resize(p=1.0, height=224, width=224, interpolation=1),
          Normalize(p=1.0, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, normalization='standard'),
        ], p=1.0, bbox_params=None, keypoint_params=None, additional_targets={}, is_check_shapes=True)

        Here, we provide an example to illustrate how to use your customized JsonEncoder to serialize the object and to
        take the indent in json to get a more readable string.
    """
    try:
        return json.dumps(
            obj=obj,
            indent=kwargs.pop("indent", 4),
            cls=encoder or json.JSONEncoder,
            ensure_ascii=kwargs.pop("ensure_ascii", False),
            **kwargs
        )
    except TypeError:
        # if the obj cannot be serialized
        return repr(obj)

def _log(message: Any, *messages: Any, level: str, sep: str = " ", pretty: bool = False, **kwargs: Any) -> None:
    pretty_func = prettify if pretty else str
    getattr(_logger, level)(sep.join(pretty_func(m) for m in (message, *messages)), **kwargs)

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
    opt = _logger.opt
    parse = _logger.parse
    patch = _logger.patch
    remove = _logger.remove
    start = _logger.start
    stop = _logger.stop

    log = _logger.log
    critical = partial(_log, level="critical")
    debug = partial(_log, level="debug")
    info = partial(_log, level="info")
    warning = partial(_log, level="warning")
    error = partial(_log, level="error")
    exception = partial(_log, level="exception")
    success = partial(_log, level="success")
    trace = partial(_log, level="trace")

@export
def load_text(pathname: PathLike, mode: str = "r", encoding: str = None, **kwargs: Any) -> AnyStr:
    with open(pathname, mode, encoding=encoding or sys.getdefaultencoding(), **kwargs) as fp:
        return fp.read()

@export
def dump_text(text: AnyStr, pathname: PathLike, mode: str = "w", encoding: str = None, **kwargs: Any) -> None:
    with open(pathname, mode, encoding=encoding or sys.getdefaultencoding(), **kwargs) as fp:
        fp.write(text)

@export
def load_json(pathname: PathLike, loader: Optional[Callable] = None, **kwargs: Any) -> Any:
    with open(pathname, "r", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        return (loader or json.load)(fp, **kwargs)

@export
def dump_json(obj: Any, pathname: PathLike, dumper: Optional[Callable] = None, **kwargs: Any) -> None:
    with open(pathname, "w", encoding=kwargs.pop("encoding", sys.getdefaultencoding())) as fp:
        return (dumper or json.dump)(obj, fp, **kwargs)

@export
def load_pickle(pathname: PathLike, **kwargs: Any) -> Any:
    with open(pathname, "rb") as fp:
        return pickle.load(fp, **kwargs)

@export
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

@export
def get_ext(pathname: PathLike) -> str:
    return os.path.splitext(pathname)[1]

@export
def get_parent(pathname: PathLike) -> str:
    return os.path.dirname(os.path.abspath(pathname))

@export
def get_filename(pathname: PathLike) -> str:
    return os.path.splitext(os.path.basename(pathname))[0]

@export
def get_basename(pathname: PathLike) -> str:
    return os.path.basename(pathname)

@export
def tuplify(obj: Any) -> Tuple[Any]:
    """Coverts an object into a tuple object. The rules of conversion are as follows:
        a) if the `obj` is an iterable except str, each element of it will be pushed into a new tuple;
        b) if the `obj` is a type other than a, e.g. str, it will be wrapped with tuple.
    """
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return tuple(obj)
    return (obj,)

@export
def listify(obj: Any) -> List[Any]:
    """Coverts an object into a list object. The rules of conversion are as follows:
        a) if the `obj` is an iterable except str, each element of it will be pushed into a new list;
        b) if the `obj` is a type other than a, e.g. str, it will be wrapped with list.
    """
    if isinstance(obj, Iterable) and not isinstance(obj, (str, bytes)):
        return list(obj)
    return [obj, ]

@export
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

@export
def attrify(d: Optional[Dict | Iterable] = None, **kwargs: Any) -> AttrDict:
    return AttrDict(d, **kwargs)
