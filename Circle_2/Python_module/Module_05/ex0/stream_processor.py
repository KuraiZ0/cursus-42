"""
Module stream_processor.

This module defines a foundation for polymorphic data processing, including
numeric, text, and log processors.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    """Abstract base class defining the common processing interface."""

    @abstractmethod
    def process(self, data: Any) -> str:
        """Process the data and return a result string."""
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate if data is appropriate for this processor."""
        pass

    def format_output(self, result: str) -> str:
        """Format the output string."""
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """Specialized processor for numeric lists."""

    def process(self, data: Any) -> str:
        """Calculate the sum and average of a list of numbers."""
        print(f"Processing data: {data}")
        if not self.validate(data):
            return "ERROR: Invalid numeric data"
        nums: List[float] = data
        total = sum(nums)
        avg = total / len(nums)
        result = (f"Processed {len(nums)} numeric values, "
                  f"sum={total}, avg={avg}")
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        """Verify that data is a list of numbers."""
        try:
            if not isinstance(data, list) or not data:
                raise ValueError
            for x in data:
                if not isinstance(x, (int, float)):
                    raise ValueError
            print("Validation: Numeric data verified")
            return True
        except (ValueError, TypeError):
            print("ERROR: Invalid numeric data")
            return False


class TextProcessor(DataProcessor):
    """Specialized processor for text strings."""

    def process(self, data: Any) -> str:
        """Analyze text length and word count."""
        print(f'Processing data: "{data}"')
        if not self.validate(data):
            return "ERROR: Invalid text data"
        length = len(data)
        words = len(data.split())
        result = f"Processed text: {length} characters, {words} words"
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        """Verify that data is a non-empty string."""
        try:
            if not isinstance(data, str) or not data:
                raise ValueError
            print("Validation: Text data verified")
            return True
        except (ValueError, TypeError):
            print("ERROR: Invalid text data")
            return False


class LogProcessor(DataProcessor):
    """Specialized processor for log messages."""

    def process(self, data: Any) -> str:
        """Process logs and detect alert levels."""
        print(f'Processing data: "{data}"')
        if not self.validate(data):
            return "ERROR: Invalid log data"

        if "ERROR" in data:
            parts = data.split("ERROR: ", 1)
            msg = parts[1] if len(parts) > 1 else data
            result = f"[ALERT] ERROR level detected: {msg}"
        elif "INFO" in data:
            result = f"[INFO] INFO level detected: {data}"
        else:
            length = len(data)
            words = len(data.split())
            result = f"Process log: {length} characters, {words} words"
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        """Verify that the log is a valid string."""
        try:
            if not isinstance(data, str) or not data:
                raise ValueError
            print("Validation: Log entry verified")
            return True
        except (ValueError, TypeError):
            print("ERROR: Invalid log data")
            return False


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")

    print("\nInitializing Numeric Processor...")
    num_p = NumericProcessor()
    print(num_p.process([1, 2, 3, 4, 5]))

    print("\nInitializing Text Processor...")
    str_p = TextProcessor()
    print(str_p.process("Hello Nexus World"))

    print("\nInitializing Log Processor...")
    log_p = LogProcessor()
    print(log_p.process("ERROR: Connection timeout"))
    print()

    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")
    demo_num = NumericProcessor()
    demo_txt = TextProcessor()
    demo_log = LogProcessor()

    print(f"Result 1: {demo_num.process([4, 42, 420])}")
    print(f"Result 2: {demo_txt.process('Just do it !')}")
    print(f"Result 3: {demo_log.process('[INFO] System ready')}")
    print()

    print("Foundation systems online. Nexus ready for advanced streams.")