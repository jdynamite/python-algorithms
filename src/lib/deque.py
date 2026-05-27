from typing import Protocol

from .generic import T


# a.k.a Double Ended Queue
class DequeADT(Protocol[T]):
    def push_front(self, data: T) -> None:
        ...

    def push_back(self, data: T) -> None:
        ...

    def pop_front(self) -> T:
        ...

    def pop_back(self) -> T:
        ...

    def peek_front(self) -> T | None:
        ...

    def peek_back(self) -> T | None:
        ...

    def is_empty(self) -> bool:
        ...

    def get_length(self) -> int:
        ...
