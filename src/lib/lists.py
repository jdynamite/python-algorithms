from typing import Generator, Generic, Protocol, TypeVar, Optional
from collections.abc import Hashable
from dataclasses import dataclass, field

T_con = TypeVar('T_con', bound=Hashable)


class ListADT(Protocol[T_con]):
    def append(self, item: T_con) -> None:
        ...

    def prepend(self, item: T_con) -> None:
        ...

    def insert_after(self, item: T_con) -> None:
        ...

    def remove(self, item: T_con) -> bool:
        ...

    def pop(self) -> Optional[T_con]:
        ...

    def contains(self, item: T_con) -> bool:
        ...

    def print(self) -> None:
        ...

    def sort(self) -> None:
        ...

    def is_empty(self) -> bool:
        ...

    def get_length(self) -> int:
        ...


@dataclass
class LinkedNode(Generic[T_con]):
    data: T_con
    next: Optional['LinkedNode']

    def __hash__(self) -> int:
        return hash((self.data, self.next))

    def get_next(self) -> Optional['LinkedNode']:
        if self.next:
            return self.next
        return None


@dataclass
class LinkedList(Generic[T_con]):
    head: Optional['LinkedNode'] = field(init=False, default=None)
    tail: Optional['LinkedNode'] = field(init=False, default=None)
    length: int = 0

    def __init__(self, *items: T_con):
        for it in items:
            self.append(it)

    def traverse(
        self
    ) -> Generator[tuple[LinkedNode, Optional[LinkedNode]], None, None]:
        if self.head is not None:
            head, tail = (self.head, self.tail)
            prev, next = (head, head.get_next())

            yield prev, next

            while prev != tail:
                if next is not None:
                    prev = next
                    next = next.get_next()
                yield prev, next

            return

        raise ValueError(f'List is empty.')

    def get_length(self) -> int:
        return self.length

    def is_empty(self) -> bool:
        return self.get_length() == 0

    def remove(self, item: T_con) -> bool:
        if self.is_empty():
            return False

        removed = False

        if self.head.data == item:
            self.head = self.head.next
            self.length -= 1
            removed = True
        else:
            for prev, next in self.traverse():
                if next is None:
                    return False

                if next.data == item:
                    self.tail = prev
                    prev.next = next.next
                    self.length -= 1
                    removed = True
                    break

        if removed:
            if self.length == 1:
                n = self.head or self.tail
                self.head = self.tail = n
            elif self.is_empty():
                self.head = self.tail = None

        return removed

    def pop(self) -> Optional[T_con]:
        # in a singuarly linked list, pop is O(n)
        if self.tail is not None:
            data = self.tail.data
            if self.remove(self.tail.data):
                return data

    def append(self, data: T_con) -> None:
        node = LinkedNode(data=data, next=None)
        self.append_node(node=node)
        self.length += 1

    def prepend(self, data: T_con) -> None:
        node = LinkedNode(data=data, next=None)
        self.prepend_node(node=node)
        self.length += 1

    def append_node(self, node: LinkedNode):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def prepend_node(self, node: LinkedNode):
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head = node
