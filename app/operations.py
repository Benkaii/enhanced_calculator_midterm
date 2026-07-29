from abc import ABC, abstractmethod
from app.exceptions import OperationError


class Operation(ABC):
    """Base class for calculator operations."""

    @abstractmethod
    def execute(self, a, b):
        pass  # pragma: no cover


class AddOperation(Operation):
    def execute(self, a, b):
        return a + b


class SubtractOperation(Operation):
    def execute(self, a, b):
        return a - b


class MultiplyOperation(Operation):
    def execute(self, a, b):
        return a * b


class DivideOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a / b


class PowerOperation(Operation):
    def execute(self, a, b):
        return a ** b


class RootOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Root degree cannot be zero")
        if a < 0 and b % 2 == 0:
            raise OperationError("Cannot take even root of negative number")
        return a ** (1 / b)

class ModulusOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot calculate modulus by zero")
        return a % b


class IntegerDivideOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot divide by zero")
        return a // b


class PercentageOperation(Operation):
    def execute(self, a, b):
        if b == 0:
            raise OperationError("Cannot calculate percentage with zero")
        return (a / b) * 100


class AbsoluteDifferenceOperation(Operation):
    def execute(self, a, b):
        return abs(a - b)