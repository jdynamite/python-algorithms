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

    def as_list(self) -> list[T]:
        data: list[T] = []
        for n, _ in self.traverse():
            data.append(n.data)
        return data

    def __list__(self) -> list[T]:
        return self.as_list()

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
        prev = None
        current = self.head

        while current is not None:
            if current.data == item:
                self.remove_node_after(prev)
                self.length -= 1
                return True
            
            prev = current
            current = current.next
        
        return False

    def pop(self) -> T | None:
        # in a singuarly linked list, pop is O(n)
        if self.tail is not None:
            data = self.tail.data
            if self.remove(self.tail.data):
                return data

    def contains(self, item: T) -> bool:
        current = self.head

        while current is not None:
            if current.data == item:
                return True
            current = current.next
        
        return False
    
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
            chain = '->'.join(map(str, self.as_list()))

        print(f'{self.__class__.__name__}([{chain}])')

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


@dataclass
class DoubleLinkNode(Generic[T]):
    data: T
    prev: DoubleLinkNode[T] | None = None
    next: DoubleLinkNode[T] | None = None


@dataclass
class DoubleLinkList(Generic[T]):
    head: DoubleLinkNode[T] | None = field(init=False)
    tail: DoubleLinkNode[T] | None = field(init=False)
    length: int = 0

    def __init__(self, *items: T):
        for it in items:
            self.append(it)
    
    def as_list(self) -> list[T]:
        data: list[T] = []
        current_node = self.head
        while current_node != None:
            data.append(current_node.data)
        return data

    def __list__(self) -> list[T]:
        return self.as_list()

    def get_length(self) -> int:
        return self.length

    def is_empty(self) -> bool:
        return self.get_length() == 0
    
    def append(self, data: T) -> None:
        node = DoubleLinkNode(data)
        self.append_node(node)

    def append_node(self, node: DoubleLinkNode[T]) -> None:
        if self.head is None and self.tail is None:
            self.head = self.tail = node
            self.length = 1
            return  

        if self.tail is None or self.head is None:
            raise RuntimeError()

        self.tail.next = node
        node.prev = self.tail
        self.tail = node

        self.length += 1

    def search(self, data: T) -> DoubleLinkNode[T] | None:
        current_node = self.head
        while current_node != None:
            if current_node.data == data:
                return current_node
            current_node = current_node.next

    def print(self):
        if self.is_empty():
            chain = ''
        elif self.get_length() == 1:
            chain = f'{self.head.data}->None'
        else:
            chain = '->'.join(map(str, self.as_list()))

        print(f'{self.__class__.__name__}([{chain}])')
