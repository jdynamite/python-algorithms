from dataclasses import dataclass


@dataclass
class KnapscakItem:
    weight: int
    value: int

    def get_weight(self) -> int:
        return self.weight

    def get_value(self) -> int:
        return self.value


def knapsack01(
    available_items: list[KnapscakItem],
    max_weight: int,
) -> list[KnapscakItem]:
    """
    Based on zyBooks' 1.10: Heuristics, exemplifies
    an algorithm using a heuristic that sacrifices optimality for speed.

    In this case, this algorithm just grabs as many valuable items as it can,
    without concern for their weight (so long as the knapsack can hold them.)
    """
    knapsack = []
    sorted_available_items = sorted(
        available_items,
        key=KnapscakItem.get_value,
        reverse=True,
    )

    remaining_weight = max_weight
    for item in sorted_available_items:
        if item.weight <= remaining_weight:
            knapsack.append(item)
            remaining_weight -= item.weight
        else:
            break

    return knapsack
