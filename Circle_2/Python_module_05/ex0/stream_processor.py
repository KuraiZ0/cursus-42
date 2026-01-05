# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    stream_processor.py                                :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/18 14:10:05 by ialmani           #+#    #+#             #
#    Updated: 2025/12/18 14:10:06 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#

from typing import Any, List
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return result


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f"Processing data: {data}")
        if not self.validate(data):
            return "ERROR: Invalid numeric data"
        nums: List[float] = data
        total = sum(nums)
        avg = total / len(nums)
        result = (f"Processed {len(nums)} "
                  f"numeric values, sum={total}, avg={avg}")
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        try:
            if not data:
                raise ValueError("Data's missing.")
            nums: List[float] = data
            sum(nums)
            print("Validation: Numeric data verified")
            return True
        except (ValueError, TypeError, ZeroDivisionError):
            print("ERROR: Invalid numeric data")
            return False

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f'Processing data: "{data}"')
        if not self.validate(data):
            return "ERROR: Invalid text data"
        length = len(data)
        words = data.count(" ") + 1
        result = f"Processed text: {length} characters, {words} words"
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        try:
            if not data:
                raise ValueError("Data's missing")
            len(data)
            print("Validation: Text data verified")
            return True
        except (ValueError, TypeError):
            print("ERROR: Invalid text data")
            return False

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


class LogProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        print(f'Processing data: "{data}"')
        if not self.validate(data):
            return "ERROR: Invalid log data"
        length = len(data)
        words = data.count(" ") + 1
        if "ERROR" in data:
            result = f"[ALERT] ERROR level detected: {data}"
        elif "INFO" in data:
            result = f"[INFO] INFO level detected: {data}"
        else:
            result = f"Process log: {length} characters, {words} words"
        return self.format_output(result)

    def validate(self, data: Any) -> bool:
        try:
            if not data:
                raise ValueError("Data's missing")
            len(data)
            print("Validation: Log entry verified")
            return True
        except (ValueError, TypeError):
            print("ERROR: Invalid log data")
            return False

    def format_output(self, result: str) -> str:
        return f"Output: {result}"


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
    print(f"Result 2: {demo_txt.process("Just do it !")}")
    print(f"Result 3: {demo_log.process("[INFO] INFO level detected:")}")
    print()

    print("Foundation systems online. Nexus ready for advanced streams.")
