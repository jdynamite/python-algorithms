import pytest
from lib.knapsack import KnapsackItem, fractional_knapsack, knapsack01


@pytest.mark.parametrize(
    ('items', 'max_weight', 'expected_weight', 'expected_value'), [
        (
            [
                KnapsackItem.create(6, 25),
                KnapsackItem.create(8, 42),
                KnapsackItem.create(12, 60),
                KnapsackItem.create(18, 95),
            ], 40, 38, 197
        ),
    ]
)
def test_knapsack01(items, max_weight, expected_weight, expected_value):
    knapsack = knapsack01(items, max_weight)
    assert sum(map(KnapsackItem.get_weight, knapsack)) == expected_weight
    assert sum(map(KnapsackItem.get_value, knapsack)) == expected_value


@pytest.mark.parametrize(
    ('items', 'max_weight', 'expected_weight', 'expected_value'), [
        (
            [
                KnapsackItem.create(6, 25),
                KnapsackItem.create(8, 42),
                KnapsackItem.create(12, 60),
                KnapsackItem.create(18, 95),
            ], 35., 35., 182
        ),
    ]
)
def test_fractional_knapsack(items, max_weight, expected_weight, expected_value):
    knapsack = fractional_knapsack(items, max_weight)
    assert sum(map(KnapsackItem.get_value, knapsack)) == expected_value
    assert sum(map(KnapsackItem.get_weight, knapsack)) == expected_weight
