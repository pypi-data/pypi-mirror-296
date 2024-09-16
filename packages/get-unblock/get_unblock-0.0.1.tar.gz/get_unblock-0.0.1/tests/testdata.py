from abc import abstractmethod
import sys
import asyncio

sys.path.append("..\\unblock")
from unblock import (
    asyncify_pp,
    asyncify,
    async_cached_property,
    async_property,
    AsyncPPBase,
    AsyncBase,
    AsyncCtxMgrBase,
    AsyncIterBase,
    AsyncPPCtxMgrBase,
    AsyncPPIterBase,
)


def test_sync_func():
    return test_sync_func.__name__


@asyncify
def asyncify_test_sync_func():
    return test_sync_func()


asyncifypp_test_sync_func = asyncify_pp(test_sync_func)


async def test_async_func():
    await asyncio.sleep(0)
    return test_async_func.__name__


class TestClass:
    @staticmethod
    def sync_static_method():
        return TestClass.sync_static_method.__name__

    @classmethod
    def sync_class_method(cls):
        return f"{cls.__name__}.{TestClass.sync_class_method.__name__}"

    def __init__(self, a) -> None:
        self.a = a

    def sync_method(self):
        return self.sync_method.__name__

    async def async_method(self):
        await asyncio.sleep(0)
        return self.async_method.__name__


class TestAbstractClass:
    def __init__(self, a) -> None:
        self.a = a

    @abstractmethod
    def sync_abstract_method(self):
        pass


class TestIterClass:
    @staticmethod
    def sync_static_method():
        return TestIterClass.sync_static_method.__name__

    @classmethod
    def sync_class_method(cls):
        return f"{cls.__name__}.{TestIterClass.sync_class_method.__name__}"

    def __init__(self, start, end) -> None:
        self.start = start
        self.end = end

    def sync_method(self):
        return self.sync_method.__name__

    def __iter__(self):
        return self

    def __next__(self):
        st = self.start
        self.start += 1
        if st >= self.end:
            raise StopIteration()
        return st


class TestCtxMgrClass:
    @staticmethod
    def sync_static_method():
        return TestCtxMgrClass.sync_static_method.__name__

    @classmethod
    def sync_class_method(cls):
        return f"{cls.__name__}.{TestCtxMgrClass.sync_class_method.__name__}"

    def __init__(self) -> None:
        self.is_done = False

    def sync_method(self):
        return self.sync_method.__name__

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.is_done = True


@asyncify
class TestClassAsyncify:
    @staticmethod
    def sync_static_method():
        return TestClassAsyncify.sync_static_method.__name__

    @classmethod
    def sync_class_method(cls):
        return f"{cls.__name__}.{TestClassAsyncify.sync_class_method.__name__}"

    def __init__(self, a) -> None:
        self.a = a

    def sync_method(self):
        return self.sync_method.__name__

    async def async_method(self):
        await asyncio.sleep(0)
        return self.async_method.__name__


class TestAsyncProperty:
    def __init__(self, val) -> None:
        self._prop = val

    def set_prop(self, val):
        self._prop = val

    @async_property
    def prop(self):
        return self._prop

    @async_cached_property
    def cached_prop(self):
        return self._prop


class TestClassAsyncWrapper(TestClass, AsyncBase):
    @staticmethod
    def _unblock_methods_to_asynchify():
        return [
            "sync_static_method",
            "sync_class_method",
            "sync_method",
            "async_method",
        ]


class TestClassAsyncPPWrapper(TestClass, AsyncPPBase):
    @staticmethod
    def _unblock_methods_to_asynchify():
        methods = [
            "sync_static_method",
            "sync_class_method",
            "sync_method",
            "async_method",
        ]
        return methods


class TestIterClassAsyncWrapper(TestIterClass, AsyncIterBase):
    pass


class TestIterClassAsyncPPWrapper(TestIterClass, AsyncPPIterBase):
    pass


class TestCtxMgrClassAsyncWrapper(TestCtxMgrClass, AsyncCtxMgrBase):
    def __init__(self) -> None:
        super().__init__()
        self.is_async_done = False

    async def aclose(self):
        await asyncio.sleep(0)
        self.is_async_done = True


class TestCtxMgrClassAsyncWrapper2(TestCtxMgrClass, AsyncCtxMgrBase):
    call_close_on_exit = False

    def __init__(self) -> None:
        super().__init__()
        self.is_async_done = False

    async def aclose(self):
        await asyncio.sleep(0)
        self.is_async_done = True


class TestCtxMgrClassAsyncPPWrapper(TestCtxMgrClass, AsyncPPCtxMgrBase):
    def __init__(self) -> None:
        super().__init__()
        self.is_async_done = False

    async def aclose(self):
        await asyncio.sleep(0)
        self.is_async_done = True


class TestCtxMgrClassAsyncPPWrapper2(TestCtxMgrClass, AsyncPPCtxMgrBase):
    call_close_on_exit = False

    def __init__(self) -> None:
        super().__init__()
        self.is_async_done = False

    async def aclose(self):
        await asyncio.sleep(0)
        self.is_async_done = True
