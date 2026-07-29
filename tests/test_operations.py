import pytest

from app.exceptions import OperationError
from app.operations import (
    AddOperation,
    SubtractOperation,
    MultiplyOperation,
    DivideOperation,
    PowerOperation,
    RootOperation,
    ModulusOperation,
    IntegerDivideOperation,
    PercentageOperation,
    AbsoluteDifferenceOperation,
)


@pytest.mark.parametrize(
    "operation, a, b, expected",
    [
        (AddOperation(), 5, 3, 8),
        (SubtractOperation(), 5, 3, 2),
        (MultiplyOperation(), 5, 3, 15),
        (DivideOperation(), 6, 3, 2),
        (PowerOperation(), 2, 3, 8),
        (RootOperation(), 9, 2, 3),
        (ModulusOperation(), 10, 3, 1),
        (IntegerDivideOperation(), 10, 3, 3),
        (PercentageOperation(), 25, 100, 25),
        (AbsoluteDifferenceOperation(), 10, 4, 6),
    ],
)
def test_operations(operation, a, b, expected):
    assert operation.execute(a, b) == expected


def test_divide_by_zero():
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        DivideOperation().execute(5, 0)


def test_root_degree_zero():
    with pytest.raises(OperationError, match="Root degree cannot be zero"):
        RootOperation().execute(9, 0)


def test_even_root_negative_number():
    with pytest.raises(OperationError, match="Cannot take even root of negative number"):
        RootOperation().execute(-9, 2)


def test_modulus_by_zero():
    with pytest.raises(OperationError, match="Cannot calculate modulus by zero"):
        ModulusOperation().execute(5, 0)


def test_integer_divide_by_zero():
    with pytest.raises(OperationError, match="Cannot divide by zero"):
        IntegerDivideOperation().execute(5, 0)


def test_percentage_by_zero():
    with pytest.raises(OperationError, match="Cannot calculate percentage with zero"):
        PercentageOperation().execute(50, 0)