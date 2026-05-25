from __future__ import annotations
from typing import Protocol, Generic
from dataclasses import dataclass, field
from logging import getLogger
from .generic import T

log = getLogger()


class StackADT(Protocol[T]):
    def push(self, data: T) -> None:
        pass

    def pop(self) -> T | None:
        pass


@dataclass
class StackNode(Generic[T]):
    data: T
    next_node: StackNode[T] | None = field(init=False, default=None)


@dataclass
class Stack(Generic[T]):
    top: StackNode[T] | None = field(init=False, default=None)

    def push(self, data: T) -> None:
        new_node = StackNode(data=data)
        new_node.next_node = self.top
        self.top = new_node

    def pop(self) -> T | None:
        if top := self.top:
            self.top = top.next_node
            log.debug(f'Top data is: {top.data}')
            return top.data
