from typing import (
    Protocol,
    Hashable,
    TypeVar,
)


class Sortable(Protocol):
    def __lt__(self, other: 'Sortable') -> bool:
        ...


class SortableHashable(Sortable, Hashable):
    pass


T = TypeVar('T', bound=SortableHashable)
