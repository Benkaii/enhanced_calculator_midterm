## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Benkaii/enhanced_calculator_midterm.git
cd enhanced_calculator_midterm
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Configuration

The application uses **python-dotenv** to load configuration from a `.env` file.

Example `.env` file:

```ini
HISTORY_FILE=history.csv
AUTO_SAVE=true
CALCULATOR_LOG_FILE=calculator.log

CALCULATOR_LOG_DIR=logs
CALCULATOR_HISTORY_DIR=history
CALCULATOR_MAX_HISTORY_SIZE=1000
CALCULATOR_PRECISION=2
CALCULATOR_MAX_INPUT_VALUE=1000000
CALCULATOR_DEFAULT_ENCODING=utf-8
```

## Running the Application

```bash
python -m app.calculator_repl
```

The calculator starts with:

```text
Welcome to the Enhanced Calculator.
Type help for available commands.
```

## Supported Commands

### Arithmetic Operations

- add
- subtract
- multiply
- divide
- power
- root
- modulus
- int_divide
- percent
- abs_diff

### Calculator Commands

- help
- history
- clear
- undo
- redo
- save
- load
- exit

## Example

```text
Enter command or operation: add
Enter first number: 3
Enter second number: 4

Result: 7.0
```

## History Management

The calculator stores history using a pandas DataFrame.

Each calculation stores:

- operation
- first operand
- second operand
- result

History supports:

- Display
- Undo
- Redo
- Save to CSV
- Load from CSV
- Automatic saving

## Logging

The application uses Python's built-in logging module.

Each calculation is written to a log file containing:

- Timestamp
- Logging level
- Operation
- Operands
- Result

Example:

```text
2026-07-28 12:00:00 INFO Operation:add OperandA:2 OperandB:3 Result:5
```

## Error Handling

The application includes validation and custom exceptions for:

- Invalid numbers
- Unsupported operations
- Division by zero
- Modulus by zero
- Integer division by zero
- Percentage division by zero
- Invalid root values
- Invalid configuration settings

## Testing

Run all tests:

```bash
pytest -v
```

Run coverage:

```bash
pytest --cov=app --cov-report=term-missing
```

Current project status:

- 96 passing tests
- 100% code coverage

## Continuous Integration

GitHub Actions automatically:

- Checks out the repository
- Sets up Python
- Installs dependencies
- Runs pytest
- Measures coverage
- Fails if coverage drops below the required threshold

## Git Usage

Development was tracked through descriptive commits documenting major milestones including:

- Additional arithmetic operations
- REPL improvements
- Logging implementation
- Observer integration
- Unit testing
- Documentation improvements

## Author

Ismael Albilal