from app.calculation import CalculationFactory
from app.calculator_config import CalculatorConfig
from app.calculator_memento import CalculatorCaretaker, CalculatorMemento
from app.exceptions import CalculatorError
from app.history import CalculationHistory
from app.input_validators import InputValidator
from app.logger import setup_logger


class LoggingObserver:
    """Logs each completed calculation."""

    def __init__(self, logger):
        self.logger = logger

    def update(self, calculator):
        latest_record = calculator.history.get_history().iloc[-1]

        self.logger.info(
            "Operation: %s, Operand A: %s, Operand B: %s, Result: %s",
            latest_record["operation"],
            latest_record["a"],
            latest_record["b"],
            latest_record["result"],
        )


class AutoSaveObserver:
    """Automatically saves history after a calculation."""

    def update(self, calculator):
        if calculator.config.is_auto_save_enabled():
            calculator.history.save_to_csv(calculator.config.history_file)


class Calculator:
    """Facade for the enhanced calculator application."""

    def __init__(self):
        self.config = CalculatorConfig()
        self.config.validate()
        self.history = CalculationHistory()
        self.caretaker = CalculatorCaretaker()
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update(self)

    def show_help(self):
        print("\nCommands:")
        print(
            "add, subtract, multiply, divide, power, root, "
            "modulus, int_divide, percent, abs_diff"
        )
        print("help, history, clear, undo, redo, save, load, exit\n")

    def show_history(self):
        history_data = self.history.get_history()

        if history_data.empty:
            print("No history available.")
            return

        print(history_data.to_string(index=False))

    def execute_calculation(self, operation, first_value, second_value):
        a = InputValidator.validate_number(first_value)
        b = InputValidator.validate_number(second_value)

        self.caretaker.save_state(
            CalculatorMemento(self.history.get_history())
        )

        calculation = CalculationFactory.create(operation, a, b)
        result = calculation.perform()

        self.history.add_record(operation, a, b, result)
        self.notify_observers()

        return result

    def clear_history(self):
        self.caretaker.save_state(
            CalculatorMemento(self.history.get_history())
        )
        self.history.clear()
        print("History cleared.")

    def undo(self):
        restored = self.caretaker.undo(self.history.get_history())
        self.history.history = restored
        print("Undo complete.")

    def redo(self):
        restored = self.caretaker.redo(self.history.get_history())
        self.history.history = restored
        print("Redo complete.")

    def save(self):
        self.history.save_to_csv(self.config.history_file)
        print("History saved.")

    def load(self):
        self.history.load_from_csv(self.config.history_file)
        print("History loaded.")

    def handle_command(self, command):
        if command == "help":
            self.show_help()
            return True

        if command == "history":
            self.show_history()
            return True

        if command == "clear":
            self.clear_history()
            return True

        if command == "undo":
            self.undo()
            return True

        if command == "redo":
            self.redo()
            return True

        if command == "save":
            self.save()
            return True

        if command == "load":
            self.load()
            return True

        return False

    def run(self):
        print("Welcome to the Enhanced Calculator.")
        print("Type help for available commands.")

        while True:
            command = input("Enter command or operation: ").lower().strip()

            if command == "exit":
                print("Goodbye!")
                break

            if InputValidator.is_valid_command(command):
                self.handle_command(command)
                continue

            if not InputValidator.is_valid_operation(command):
                print("Invalid command or operation.")
                continue

            try:
                first_value = input("Enter first number: ")
                second_value = input("Enter second number: ")

                result = self.execute_calculation(
                    command,
                    first_value,
                    second_value,
                )

                print(f"Result: {result}")

            except CalculatorError as error:
                print(f"Error: {error}")


def main():
    calculator = Calculator()

    logger = setup_logger()
    calculator.add_observer(LoggingObserver(logger))
    calculator.add_observer(AutoSaveObserver())

    calculator.run()


if __name__ == "__main__":  # pragma: no cover
    main()