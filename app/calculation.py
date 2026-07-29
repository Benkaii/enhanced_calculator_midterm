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
from app.exceptions import OperationError


class Calculation:
    """Represents a calculation using an operation strategy."""

    def __init__(self, operation_name, a, b, operation):
        self.operation_name = operation_name
        self.a = a
        self.b = b
        self.operation = operation

    def perform(self):
        """Execute the selected calculation operation."""
        return self.operation.execute(self.a, self.b)


class CalculationFactory:
    """Factory for creating calculation objects."""

    operations = {
        "add": AddOperation,
        "subtract": SubtractOperation,
        "multiply": MultiplyOperation,
        "divide": DivideOperation,
        "power": PowerOperation,
        "root": RootOperation,
        "modulus": ModulusOperation,
        "int_divide": IntegerDivideOperation,
        "percent": PercentageOperation,
        "abs_diff": AbsoluteDifferenceOperation,
    }

    @classmethod
    def create(cls, operation_name, a, b):
        """Create a calculation using the requested operation."""

        if operation_name not in cls.operations:
            raise OperationError("Invalid operation")

        operation = cls.operations[operation_name]()

        return Calculation(
            operation_name,
            a,
            b,
            operation,
        )