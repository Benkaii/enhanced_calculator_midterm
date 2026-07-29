import pandas as pd
import pytest
from unittest.mock import patch

from app.calculator_repl import (
    AutoSaveObserver,
    Calculator,
    LoggingObserver,
    main,
)
from app.logger import setup_logger


def test_calculator_initializes():
    calculator = Calculator()

    assert calculator.config is not None
    assert calculator.history is not None
    assert calculator.caretaker is not None
    assert calculator.observers == []


def test_add_observer():
    calculator = Calculator()
    observer = AutoSaveObserver()

    calculator.add_observer(observer)

    assert observer in calculator.observers


def test_observer_auto_save_enabled(tmp_path, monkeypatch):
    file_path = tmp_path / "history.csv"
    monkeypatch.setenv("HISTORY_FILE", str(file_path))
    monkeypatch.setenv("AUTO_SAVE", "true")

    calculator = Calculator()
    observer = AutoSaveObserver()

    calculator.execute_calculation("add", "2", "3")
    observer.update(calculator)

    assert file_path.exists()


def test_observer_auto_save_disabled(tmp_path, monkeypatch):
    file_path = tmp_path / "history.csv"
    monkeypatch.setenv("HISTORY_FILE", str(file_path))
    monkeypatch.setenv("AUTO_SAVE", "false")

    calculator = Calculator()
    observer = AutoSaveObserver()

    calculator.execute_calculation("add", "2", "3")
    observer.update(calculator)

    assert not file_path.exists()


def test_notify_observers(tmp_path, monkeypatch):
    file_path = tmp_path / "history.csv"
    monkeypatch.setenv("HISTORY_FILE", str(file_path))
    monkeypatch.setenv("AUTO_SAVE", "true")

    calculator = Calculator()
    calculator.add_observer(AutoSaveObserver())

    calculator.execute_calculation("add", "2", "3")

    assert file_path.exists()

def test_logging_observer(tmp_path):
    log_file = tmp_path / "calculator.log"

    logger = setup_logger(str(log_file))

    calculator = Calculator()
    calculator.add_observer(LoggingObserver(logger))

    calculator.execute_calculation("add", "2", "3")

    for handler in logger.handlers:
        handler.flush()

    assert log_file.exists()

    contents = log_file.read_text()

    assert "Operation: add" in contents
    assert "Result: 5.0" in contents

def test_show_help(capsys):
    calculator = Calculator()

    calculator.show_help()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out


def test_show_history_empty(capsys):
    calculator = Calculator()

    calculator.show_history()

    captured = capsys.readouterr()
    assert "No history available." in captured.out


def test_show_history_with_data(capsys):
    calculator = Calculator()
    calculator.history.add_record("add", 2, 3, 5)

    calculator.show_history()

    captured = capsys.readouterr()
    assert "add" in captured.out


def test_execute_calculation():
    calculator = Calculator()

    result = calculator.execute_calculation("multiply", "4", "5")

    assert result == 20


def test_clear_history(capsys):
    calculator = Calculator()
    calculator.history.add_record("add", 2, 3, 5)

    calculator.clear_history()

    captured = capsys.readouterr()

    assert calculator.history.get_history().empty
    assert "History cleared." in captured.out


def test_undo_redo(capsys):
    calculator = Calculator()

    calculator.execute_calculation("add", "2", "3")
    calculator.clear_history()
    calculator.undo()
    calculator.redo()

    captured = capsys.readouterr()

    assert "Undo complete." in captured.out
    assert "Redo complete." in captured.out


def test_save_and_load(tmp_path, monkeypatch, capsys):
    file_path = tmp_path / "history.csv"
    monkeypatch.setenv("HISTORY_FILE", str(file_path))

    calculator = Calculator()
    calculator.execute_calculation("add", "2", "3")

    calculator.save()
    calculator.clear_history()
    calculator.load()

    captured = capsys.readouterr()

    assert "History saved." in captured.out
    assert "History loaded." in captured.out
    assert not calculator.history.get_history().empty


@pytest.mark.parametrize(
    "command",
    ["help", "history", "clear", "undo", "redo", "save"],
)
def test_handle_command(command):
    calculator = Calculator()

    assert calculator.handle_command(command)


def test_handle_load(tmp_path, monkeypatch):
    file_path = tmp_path / "history.csv"
    pd.DataFrame(
        [{"operation": "add", "a": 2, "b": 3, "result": 5}]
    ).to_csv(file_path, index=False)

    monkeypatch.setenv("HISTORY_FILE", str(file_path))

    calculator = Calculator()

    assert calculator.handle_command("load")


def test_handle_unknown_command():
    calculator = Calculator()

    assert not calculator.handle_command("unknown")


@patch("builtins.input", side_effect=["exit"])
def test_run_exit(mock_input, capsys):
    calculator = Calculator()

    calculator.run()

    captured = capsys.readouterr()
    assert "Goodbye!" in captured.out


@patch("builtins.input", side_effect=["bad", "exit"])
def test_run_invalid_command(mock_input, capsys):
    calculator = Calculator()

    calculator.run()

    captured = capsys.readouterr()
    assert "Invalid command or operation." in captured.out


@patch("builtins.input", side_effect=["help", "exit"])
def test_run_help_command(mock_input, capsys):
    calculator = Calculator()

    calculator.run()

    captured = capsys.readouterr()
    assert "Commands:" in captured.out


@patch("builtins.input", side_effect=["add", "2", "3", "exit"])
def test_run_add_operation(mock_input, capsys):
    calculator = Calculator()

    calculator.run()

    captured = capsys.readouterr()
    assert "Result: 5.0" in captured.out


@patch("builtins.input", side_effect=["add", "hello", "3", "exit"])
def test_run_invalid_number(mock_input, capsys):
    calculator = Calculator()

    calculator.run()

    captured = capsys.readouterr()
    assert "Input must be a number" in captured.out


@patch("builtins.input", side_effect=["divide", "5", "0", "exit"])
def test_run_divide_by_zero(mock_input, capsys):
    calculator = Calculator()

    calculator.run()

    captured = capsys.readouterr()
    assert "Cannot divide by zero" in captured.out


@patch("app.calculator_repl.Calculator.run")
def test_main(mock_run):
    main()

    mock_run.assert_called_once()