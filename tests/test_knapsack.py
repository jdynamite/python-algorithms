import pytest
from lib.knapsack_01 import KnapscakItem, knapsack01


@pytest.mark.parametrize(
    ('items', 'max_weight', 'expected_weight', 'expected_value'), [
        (
            [
                KnapscakItem(6, 25),
                KnapscakItem(8, 42),
                KnapscakItem(12, 60),
                KnapscakItem(18, 95),
            ], 40, 38, 197
        ),
    ]
)
def test_knapsack01(items, max_weight, expected_weight, expected_value):
    knapsack = knapsack01(items, max_weight)
    assert sum(map(KnapscakItem.get_weight, knapsack)) == expected_weight
    assert sum(map(KnapscakItem.get_value, knapsack)) == expected_value
