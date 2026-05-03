from dataclasses import dataclass, field, replace


@dataclass
class KnapsackItem:
    weight: float
    value: float
    fraction: float = field(default=1.0)

    @classmethod
    def create(cls, weight: int | float, value: int | float) -> 'KnapsackItem':
        return cls(float(weight), float(value))

    def get_score(self) -> float:
        return self.value / self.weight

    def get_weight(self) -> float:
        return self.weight * self.fraction

    def get_value(self) -> float:
        return self.value * self.fraction


def knapsack01(
    available_items: list[KnapsackItem],
    max_weight: int,
) -> list[KnapsackItem]:
    """
    Based on zyBooks' 1.10: Heuristics, exemplifies
    an algorithm using a heuristic that sacrifices optimality for speed.

    In this case, this algorithm just grabs as many valuable items as it can,
    without concern for their weight (so long as the knapsack can hold them.)
    """
    knapsack = []
    sorted_available_items = sorted(
        available_items,
        key=KnapsackItem.get_value,
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


def fractional_knapsack(
    available_items: list[KnapsackItem],
    max_weight: int | float,
) -> list[KnapsackItem]:
    knapsack = []
    sorted_available_items = sorted(
        available_items,
        key=KnapsackItem.get_score,
        reverse=True,
    )

    remaining = max_weight
    for item in sorted_available_items:
        if item.weight <= remaining:
            knapsack.append(item)
            remaining -= item.weight
        elif remaining > 0:
            knapsack.append(replace(item, fraction=remaining/item.weight))
            break

    return knapsack
