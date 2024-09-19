from asyncio import iscoroutine
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass, field
from typing import (
    Any,
    AsyncContextManager,
    AsyncIterator,
    Awaitable,
    Callable,
    ContextManager,
    Self,
)

import injection

type RuntimeElement = (
    AsyncContextManager[Any] | ContextManager[Any] | Awaitable[None] | None
)
type RuntimeElementFactory = Callable[..., RuntimeElement]


@injection.constant(mode="fallback")
@dataclass(repr=False, eq=False, frozen=True, slots=True)
class Runtime:
    __factories: list[RuntimeElementFactory] = field(
        default_factory=list,
        init=False,
    )

    @property
    @asynccontextmanager
    async def lifespan(self) -> AsyncIterator[None]:
        async with AsyncExitStack() as stack:
            for factory in self.__factories:
                el = factory()

                if iscoroutine(el):
                    await el

                elif isinstance(el, AsyncContextManager):
                    await stack.enter_async_context(el)

                elif isinstance(el, ContextManager):
                    stack.enter_context(el)

            yield

    def add_elements(self, *factories: RuntimeElementFactory) -> Self:
        self.__factories.extend(factories)
        return self


@dataclass(eq=False, frozen=True, slots=True)
class RuntimeElementDecorator:
    injection_module: injection.Module = field(default_factory=injection.mod)

    def __call__(self, wrapped: RuntimeElementFactory | None = None, /):  # type: ignore[no-untyped-def]
        def decorator(wp):  # type: ignore[no-untyped-def]
            factory = self.injection_module.make_injected_function(wp)
            self.__find_runtime().add_elements(factory)
            return wp

        return decorator(wrapped) if wrapped else decorator

    def __find_runtime(self) -> Runtime:
        return self.injection_module.find_instance(Runtime)


runtime_element = RuntimeElementDecorator()
