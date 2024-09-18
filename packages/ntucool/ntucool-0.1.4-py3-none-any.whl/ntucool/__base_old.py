from __future__ import annotations

import asyncio
import http
import logging
from abc import ABCMeta, abstractmethod
from collections import defaultdict
from functools import wraps
from typing import (
    Any,
    Callable,
    DefaultDict,
    Literal,
    Self,
    dataclass_transform,
    final,
    override,
)

import greenback
import httpx
from pydantic import BaseModel, ConfigDict, Field

from ntucool.requestor import Requestor


class _RemoteProperty:
    pass


def remote_property(init: Literal[False] = False) -> Any:
    return _RemoteProperty()


def page_field(init: bool) -> Any: ...


_INNER_TYPE = "__type__"
_INNER_INSTANCE = "__inner__"
_REMOTE_PROPS = "__remote_props__"

i = 0


@dataclass_transform(
    kw_only_default=True,
    field_specifiers=(remote_property,),
)
class PageObjectMetaclass(ABCMeta):
    def __new__(
        cls, name: str, bases: tuple[type, ...], attrs: dict[str, Any], **kwargs
    ):
        # if not bases:
        #     return type.__new__(cls, name, bases, attrs)

        remote_props = {
            k: v for k, v in attrs.items() if isinstance(v, _RemoteProperty)
        }
        for base in bases:
            remote_props |= {k: None for k in getattr(base, _REMOTE_PROPS)}
        attrs_filtered = {
            k: v for k, v in attrs.items() if not isinstance(v, _RemoteProperty)
        }

        # print(name)
        # if bases:
        #     print(remote_props, getattr(bases[0], _REMOTE_PROPS))

        inner = "__" + name + "Inner"

        def __init_inner__(self: object, **kwargs):
            # global i
            # i += 1
            # if i > 2:
            #     exit()

            # if (init:=attrs.get('__init__',None)):
            #     init(self)
            # else:
            super(self.__class__, self).__init__()

            for k, v in kwargs.items():
                if k in remote_props:
                    raise Exception(
                        f"Property `{k}` is remote and should not be initialized."
                    )
                setattr(self, k, v)

        __type__ = type.__new__(
            cls,
            inner,
            bases,
            attrs
            | {
                "__qualname__": inner,
                "__init__": __init_inner__,
            },
        )

        def __init__(self, **kwargs):
            inner_instance = __type__.__new__(__type__, **kwargs)  # type: ignore
            inner_instance.__init__(**kwargs)  # type: ignore
            setattr(self, _INNER_INSTANCE, inner_instance)

            __init_inner__(self, **kwargs)
            if init := attrs.get("__init__", None):
                init(self)

        return type.__new__(
            cls,
            name,
            bases,
            (
                attrs_filtered
                | {
                    _INNER_TYPE: __type__,
                    _REMOTE_PROPS: set(remote_props.keys()),
                }
                | (
                    {
                        "__init__": __init__,
                    }
                    if bases
                    else {}
                )
            ),
        )


_update_counter = 0


def _counter_inc():
    global _update_counter
    _update_counter += 1
    return _update_counter


class NTUCoolBase[Async: bool]:
    model_config = ConfigDict(arbitrary_types_allowed=True)

    parent: NTUCoolBase | None = Field(default=None, repr=False)
    requestor: Requestor = Field(default=None, init=False, repr=False)

    refresh_timestamp: float = Field(
        default_factory=_counter_inc, init=False, repr=False
    )
    last_update: DefaultDict[str, float] = Field(
        default_factory=lambda: defaultdict(lambda: -1),
        init=False,
        repr=False,
    )

    def __init__(self, is_async: Async = False):
        self.is_async = is_async

    def model_post_init(self, __context: Any) -> None:
        if self.parent:
            self.requestor = self.parent.requestor
            assert self.requestor
        else:
            raise Exception("No parent", self)

    # if not self.requestor and self._parent:
    #     self.requestor = self._parent.requestor

    # if self._parent and self._parent._is_async:
    #     self._is_async = True

    def __get_refresh_timestamp(self) -> float:
        if self.parent:
            res = self.parent.__get_refresh_timestamp()
            self.refresh_timestamp = res
        return self.refresh_timestamp

    def _should_update(self, name: str) -> bool:
        if self.last_update is None:
            return True
        refresh_timestamp = self.__get_refresh_timestamp()
        return self.last_update[name] < refresh_timestamp

    def refresh(self):
        self.refresh_timestamp = _counter_inc()

    is_async: bool = Field(default=False, init=False)
    portal_created: bool = Field(default=False, init=False)

    def _get_is_async(self):  # -> Any | bool:
        if self.is_async:
            return True
        if not self.parent:
            return False
        return self.parent._get_is_async()

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    async def __aenter__(self):
        await greenback.ensure_portal()
        self.portal_created = True
        self.is_async = True

        # if not self.requestor._async_client:
        #     self.requestor._async_client = httpx.AsyncClient()

        return self

    async def __aexit__(self, *exc_info):
        self.is_async = False
        return False

    def __str__(self) -> str:
        return repr(self)


class B(NTUCoolBase):
    b: int
    a: int = remote_property()


def remote_cache[T, S: NTUCoolBase](f: Callable[[S], T]) -> Callable[[S], T]:
    cache_val: T | None = None

    @wraps(f)
    def _f(*args, **kwargs):
        nonlocal cache_val
        obj: S = args[0] if args else kwargs["self"]
        if obj._should_update(f.__name__) or cache_val is None:
            cache_val = f(*args, **kwargs)
            obj.last_update[f.__name__] = _counter_inc()
        return cache_val

    return _f
