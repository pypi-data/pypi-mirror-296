from __future__ import annotations

from typing import TYPE_CHECKING, Any, Awaitable, Callable, Literal, overload

from async_property.base import AsyncPropertyDescriptor

if TYPE_CHECKING:
    from .base import NTUCoolBase


class NTUCoolDescriptor[R]:
    def __init__(
        self,
        getter: Callable[[Any], R],
        async_getter: Callable[[Any], Awaitable[R]],
    ):
        self.getter = getter
        self.async_getter = async_getter

        self.async_descriptor = AsyncPropertyDescriptor(self.async_getter)

    @overload
    def __get__(self, instance: NTUCoolBase[Literal[True]], owner) -> Awaitable[R]: ...

    @overload
    def __get__(self, instance: NTUCoolBase[Literal[False]], owner) -> R: ...

    def __get__(self, instance: NTUCoolBase, owner):  # type: ignore
        if instance._is_async:
            return self.async_descriptor.__get__(instance, owner)
        return self.getter(instance)

    def __set__(self, instance, value):
        raise ValueError("Cannot set value")

    def __delete__(self, instance):
        raise ValueError("Cannot delete value")


def test():
    async def f(x: int):
        return []

    def g(x: int):
        return []

    class A[Async: bool](NTUCoolBase[Async]):
        x = NTUCoolDescriptor(g, f)

    class B(A[Literal[True]]): ...

    class C(A[Literal[False]]): ...

    y_ = B().x
    y__ = C().x

    print(y_, y__)
