import pytest

from diofant.core.rules import Transform


def test_Transform():
    add1 = Transform(lambda x: x + 1, lambda x: x % 2 == 1)
    assert add1[1] == 2
    assert (1 in add1) is True
    assert add1.get(1) == 2

    pytest.raises(KeyError, lambda: add1[2])
    assert (2 in add1) is False
    assert add1.get(2) is None
