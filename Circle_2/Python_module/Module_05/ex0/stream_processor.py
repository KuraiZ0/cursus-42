"""Provides a basic framework for processing different types of data.

It defines a `DataProcessor` abstract base class and concrete implementations
for handling numeric, text, and log data. The module demonstrates polymorphic
processing of different data types through a unified interface.
"""

from abc import ABC, abstractmethod
from typing import Any, List


class DataProcessor(ABC):
    """An abstract base class for a data processor."""

    @abstractmethod
    def process(self, data: Any) -> str:
        """Process the given data.

        Args:
            data: The data to be processed.

        Returns:
            A string summarizing the processing results.
        """
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        """Validate the given data.

        Args:
            data: The data to be validated.

        Returns:
            True if the data is valid, False otherwise.
        """
        pass

    def format_output(self, result: str) -> str:
        """Format the output string.

        Args:
            result: The string to be formatted.

        Returns:
            The formatted output string.
        """
        return f"Output: {result}"


class NumericProcessor(DataProcessor):
    """A data processor for numeric data."""

    def process(self, data: Any) -> str:
        """Process a list of numeric data.

        Args:
            data: A list of numbers to be processed.

        Returns:
            A string summarizing the processing results.

        Raises:
            ValueError: If the data is not valid numeric data.
        """
        if not self.validate(data):
            raise ValueError("Invalid numeric data")
        total = sum(data)
        avg = total / len(data)
        return f"Processed {len(data)} numeric values, sum={total}, avg={avg}"

    def validate(self, data: Any) -> bool:
        """Validate if the data is a list of numbers.

        Args:
            data: The data to be validated.

        Returns:
            True if the data is a list of numbers, False otherwise.
        """
        try:
            if isinstance(data, list) and all(
                isinstance(x, (int, float)) for x in data
            ):
                return True
            return False
        except TypeError:
            return False


class TextProcessor(DataProcessor):
    """A data processor for text data."""

    def process(self, data: Any) -> str:
        """Process a string of text data.

        Args:
            data: A string to be processed.

        Returns:
            A string summarizing the processing results.

        Raises:
            ValueError: If the data is not valid text data.
        """
        if not self.validate(data):
            raise ValueError("Invalid text data")
        char_count: int = len(data)
        word_count: int = len(data.split())
        return f"Processed text: {char_count} characters, {word_count} words"

    def validate(self, data: Any) -> bool:
        """Validate if the data is a string.

        Args:
            data: The data to be validated.

        Returns:
            True if the data is a string, False otherwise.
        """
        return isinstance(data, str)


class LogProcessor(DataProcessor):
    """A data processor for log data."""

    def process(self, data: Any) -> str:
        """Process a string of log data.

        Args:
            data: A string representing a log message.

        Returns:
            A string summarizing the processing results.

        Raises:
            ValueError: If the data is not valid log data.
        """
        if not self.validate(data):
            raise ValueError("Invalid log data")
        if "ERROR" in data:
            level = "ERROR"
            tag = "[ALERT]"
        elif "INFO" in data:
            level = "INFO"
            tag = "[INFO]"
        else:
            level = "DEBUG"
            tag = "[DEBUG]"
        message = data.split(": ", 1)[-1] if ": " in data else data
        return f"{tag} {level} level detected: {message}"

    def validate(self, data: Any) -> bool:
        """Validate if the data is a string.

        Args:
            data: The data to be validated.

        Returns:
            True if the data is a string, False otherwise.
        """
        return isinstance(data, str)


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===")
    print()

    print("Initializing Numeric Processor...")
    num_proc = NumericProcessor()
    data1 = [1, 2, 3, 4, 5]
    print(f"Processing data: {data1}")
    validation_text = ('Numeric data verified'
                       if num_proc.validate(data1) else 'Invalid')
    print(f"Validation: {validation_text}")
    print(num_proc.format_output(num_proc.process(data1)))
    print()

    print("Initializing Text Processor...")
    text_proc = TextProcessor()
    data2 = "Hello Nexus World"
    print(f'Processing data: "{data2}"')
    validation_text = ('Text data verified'
                       if text_proc.validate(data2) else 'Invalid')
    print(f"Validation: {validation_text}")
    print(text_proc.format_output(text_proc.process(data2)))
    print()

    print("Initializing Log Processor...")
    log_proc = LogProcessor()
    data3 = "ERROR: Connection timeout"
    print(f'Processing data: "{data3}"')
    validation_text = ('Log entry verified'
                       if log_proc.validate(data3) else 'Invalid')
    print(f"Validation: {validation_text}")
    print(log_proc.format_output(log_proc.process(data3)))
    print()

    print("=== Polymorphic Processing Demo ===")
    print("Processing multiple data types through same interface...")

    processors: List[DataProcessor] = [
        NumericProcessor(),
        TextProcessor(),
        LogProcessor(),
    ]

    test_data: List[Any] = [[1, 2, 3], "Hello Nexus!", "INFO: System ready"]

    for i, (proc, data) in enumerate(zip(processors, test_data), 1):
        result = proc.process(data)
        print(f"Result {i}: {result}")

    print()
    print("Foundation systems online. Nexus ready for advanced streams.")
