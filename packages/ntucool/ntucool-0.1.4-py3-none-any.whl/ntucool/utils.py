import asyncio
import inspect
from ast import expr_context
from asyncio import coroutines
from time import time
from typing import Any, Awaitable, Callable, Coroutine, Union, overload

import greenback
from async_property import async_property


def is_in_coroutine():
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            # for frame_info in inspect.stack():
            #     if inspect.iscoroutinefunction(
            #         frame_info.frame.f_globals.get(frame_info.function, None)
            #     ):
            return True
    except RuntimeError:
        pass
    return False


async def _wrap_coroutine[T](x: Union[Awaitable[T], T]) -> T:
    await greenback.ensure_portal()
    if inspect.isawaitable(x):
        return await x
    return x  # type: ignore


# async def _no_op[T](x: T) -> T:
#     return x


@overload
def gather_[T](*obj: Awaitable[T]) -> list[T]: ...
@overload
def gather_[T](*obj: T) -> list[T]: ...
def gather_[T](*objs: Union[Awaitable[T], T]) -> Any:
    print("gather_")
    coroutines = (_wrap_coroutine(obj) for obj in objs)
    # coroutines   = objs
    print("before gather")
    g: asyncio.Future[list[T]] = asyncio.gather(*coroutines)
    # exit()
    x = await_(g)
    return x


@overload
def await_[T](obj: Awaitable[T]) -> T: ...
@overload
def await_[T](obj: T) -> T: ...
def await_(obj):
    if inspect.isawaitable(obj):
        print("\ntrying await", obj)
        try:
            return greenback.await_(obj)
        except RuntimeError as e:
            print('await_ failed', e)   
        try:
            print("current", asyncio.current_task())
            greenback.bestow_portal(asyncio.current_task())
            return greenback.await_(obj)
        except RuntimeError as e:
            print("error", e)

            # not running in async
            async def co():

                await greenback.ensure_portal()
                # print("obj", obj)
                return await obj

            return asyncio.run(co())
    return obj


async def async_retry[T](
    fn: Callable[[], Coroutine[Any, Any, T]],
    pred: Callable[[T], bool],
    delay=0.1,
    timeout=10,
) -> T:
    st = time()
    while time() - st < timeout:
        task = asyncio.create_task(fn())
        res = await_(task)
        if pred(res):
            return res
        # print(res.json()[ 'completion' ])
        await asyncio.sleep(delay)
    # todo: this may crash
    raise Exception("timeout")
