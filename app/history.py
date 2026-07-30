from datetime import datetime

import pandas as pd


class CalculationHistory:
    """Manages calculation history using pandas."""

    def __init__(self):
        """Initialize an empty calculation history DataFrame."""
        self.history = pd.DataFrame(
            columns=[
                "operation",
                "a",
                "b",
                "result",
                "timestamp",
            ]
        )

    def add_record(self, operation, a, b, result):
        """Add a calculation record with a timestamp."""
        new_record = pd.DataFrame(
            [
                {
                    "operation": operation,
                    "a": a,
                    "b": b,
                    "result": result,
                    "timestamp": datetime.now().isoformat(
                        timespec="seconds"
                    ),
                }
            ]
        )

        self.history = pd.concat(
            [self.history, new_record],
            ignore_index=True,
        )

    def clear(self):
        """Clear all calculation history."""
        self.history = self.history.iloc[0:0]

    def get_history(self):
        """Return the calculation history DataFrame."""
        return self.history

    def save_to_csv(self, file_path):
        """Save calculation history to a CSV file."""
        self.history.to_csv(file_path, index=False)

    def load_from_csv(self, file_path):
        """Load calculation history from a CSV file."""
        self.history = pd.read_csv(file_path)