import pytest
from lib.stack import Stack

@pytest.fixture
def numbers():
    return (76, 81, 91, 34, 62, 88, 77, 21, 18)

def test_stacks(numbers):
    stack = Stack()

    for n in numbers:
        stack.push(n)

    assert stack.top is not None
    assert stack.top.data == 18

    # LIFO
    for n in reversed(numbers):
        assert stack.pop() == n
