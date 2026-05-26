from __future__ import annotations
from dataclasses import dataclass, field
from typing import Generic, Protocol
from .generic import T


# As opposed to stacks, which are LIFO,
# queues are FIFO (first in, first out)

class QueueADT(Protocol[T]):
    def enqueue(self, data: T) -> None:
        ...

    def dequeue(self) -> T:
        ...

    def peek(self) -> T | None:
        ...

    def is_empty(self) -> bool:
        ...

    def get_length(self) -> int:
        ...

@dataclass
class QueueNode(Generic[T]):
    data: T
    next_node: QueueNode[T] | None = None


@dataclass
class Queue(Generic[T]):
    front: QueueNode[T] | None = field(init=False, default=None)
    end: QueueNode[T] | None = field(init=False, default=None)
    length: int = field(init=False, default=0)

    def is_empty(self) -> bool:
        return self.length == 0

    def enqueue(self, data: T) -> None:
        new_node = QueueNode(data=data)

        if self.front is None:
            self.front = new_node
        else:
            self.end.next_node = new_node

        self.end = new_node
        self.length += 1

    def dequeue(self) -> T:
        if front := self.front:
            data = front.data
            self.front = front.next_node

            if self.length <= 1:
                self.end = self.front

            self.length -= 1
            return data
        else:
            raise RuntimeError('Queue is empty!')

    def peek(self) -> T | None:
        if front := self.front:
            return front.data
