from __future__ import annotations
from typing import Generic, Protocol, TypeVar
from collections.abc import Hashable, Generator
from dataclasses import dataclass, field

from typing_extensions import override

T = TypeVar('T', bound=Hashable)


class ListADT(Protocol[T]):
    def append(self, item: T) -> None:
        ...

    def prepend(self, item: T) -> None:
        ...

    def insert_after(self, item: T) -> None:
        ...

    def remove(self, item: T) -> bool:
        ...

    def pop(self) -> T | None:
        ...

    def contains(self, item: T) -> bool:
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
class LinkedNode(Generic[T]):
    data: T
    next: LinkedNode[T] | None

    @override
    def __hash__(self) -> int:
        return hash((self.data, self.next))


@dataclass
class LinkedList(Generic[T]):
    head: LinkedNode[T] | None = field(init=False, default=None)
    tail: LinkedNode[T] | None = field(init=False, default=None)
    length: int = 0

    def __init__(self, *items: T):
        for it in items:
            self.append(it)

    def traverse(
        self
    ) -> Generator[tuple[LinkedNode[T], LinkedNode[T] | None], None, None]:
        if self.is_empty():
            raise ValueError(f'List is empty!') from None
        prev = self.head
        while prev != None:
            yield prev, prev.next 
            prev = prev.next

    def get_length(self) -> int:
        return self.length

    def is_empty(self) -> bool:
        return self.get_length() == 0

    def remove(self, item: T) -> bool:
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

    def pop(self) -> T | None:
        # in a singuarly linked list, pop is O(n)
        if self.tail is not None:
            data = self.tail.data
            if self.remove(self.tail.data):
                return data

    def append(self, data: T) -> None:
        node = LinkedNode(data=data, next=None)
        self.append_node(node=node)
        self.length += 1

    def prepend(self, data: T) -> None:
        node = LinkedNode(data=data, next=None)
        self.prepend_node(node=node)
        self.length += 1

    def remove_node_after(self, node: LinkedNode[T] | None):
        if self.head is None: # == self.is_empty():
            raise RuntimeError('The list is empty.')
        # if node is None, we're remove the current head. 
        # Special case: remove head
        if node is None:
            self.head = self.head.next
            if self.head is None:
                self.tail = None
        elif node.next != None:
            n = node.next.next
            node.next = n
            if n is None:
                self.tail = node

    def insert_after(self, data: T, new_data: T) -> bool:
        if current_node := self.search(data):
            new_node = LinkedNode(data=new_data, next=None)
            self.insert_node_after(current_node, new_node)
            return True
        return False

    def search(self, data: T) -> LinkedNode[T] | None:
        for p, _ in self.traverse():
            if p.data == data:
                return p

    def print(self):
        if self.is_empty():
            chain = ''
        elif self.get_length() == 1:
            chain = f'{self.head.data}->None'
        else:
            nodes: list[LinkedNode[T]] = [p.data for p, _ in self.traverse()] 
            chain = '->'.join(map(str, nodes))

        print(f'LinkedList([{chain}])')

    def insert_node_after(self, node: LinkedNode[T] | None, new_node: LinkedNode[T]):
        if self.head is None or node == self.tail:
            self.append_node(new_node)
        elif node:
            new_node.next = node.next
            node.next = new_node
            self.length += 1

    def append_node(self, node: LinkedNode[T]):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.tail.next = node
            self.tail = node

    def prepend_node(self, node: LinkedNode[T]):
        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head = node
