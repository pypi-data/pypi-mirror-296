from __future__ import annotations

from types import GeneratorType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any, Callable


class GenGine:
    def __init__(self, callables: list[Callable[[Any], Any]]) -> None:
        self.callables = callables

    def run(self, data_in=None) -> Generator[Any, None, None]:
        yield from self._iterate_callables(data_in=data_in, callable_idx=0)

    def _iterate_callables(self, data_in, callable_idx: int) -> Generator[Any, None, None]:
        temp_out = data_in
        idx = callable_idx
        for c in self.callables[callable_idx:]:
            if not temp_out:
                break
            temp_out = c(temp_out)
            if isinstance(temp_out, GeneratorType):
                if (idx + 1) < len(self.callables):
                    yield from self._iterate_generator(temp_out, callable_idx=(idx + 1))
                    break
                if (idx + 1) == len(self.callables):
                    yield from self._yield_non_nones(temp_out)
            elif (idx + 1) == len(self.callables):
                if temp_out:
                    # only yield if not None
                    yield temp_out
            idx += 1

    def _iterate_generator(self, generator: GeneratorType, callable_idx: int) -> Generator[Any, None, None]:
        for el in generator:
            yield from self._iterate_callables(data_in=el, callable_idx=callable_idx)

    def _yield_non_nones(self, generator: GeneratorType) -> Any:
        for el in generator:
            if el:
                yield el
