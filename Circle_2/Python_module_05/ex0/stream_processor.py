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

from typing import Any, List, Dict, Union, Optional
from abc import ABC, abstractmethod


class DataProcessor(ABC):
    @abstractmethod
    def process(self, data: Any) -> str:
        pass

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    def format_output(self, result: str) -> str:
        return "c"


class NumericProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        return (f"Processing data: {data}")

    def validate(self, data: Any) -> bool:
        if not data:
            raise NotImplementedError("ERROR: Data's missing.")
        else:
            print("Validation: Numeric data verified")
            return True

    def format_output(self, result: str) -> str:
        nums: list[float] = result
        sum_num = sum(num_p)
        avg_num = sum_num / len(num_p)
        return (f"Output: Processed {len(num_p)} numeric values, "
                f"sum={sum_num}, avg={avg_num}")


class TextProcessor(DataProcessor):
    def process(self, data: Any) -> str:
        if self.validate(data):
            return self.format_output(data)
        return (f"Processing data: {data}")

    def validate(self, data: Any) -> bool:
        if not data:
            raise NotImplementedError("ERROR: Data's missing")
        else:
            print("Validation: Text data verified")
            return True

    def format_output(self, result: str) -> str:
        len_result = len(result)
        space: int = result.count(" ")
        num_word: int = space + 1
        return (f"Output: Processed text: {len_result} characters,"
                f" {num_word} words")


class LogProcessor(DataProcessor):
    def process(self, data: Any)-> str:
        pass
    def validate(self, data: Any) -> bool:
        pass
    def format_output(self, result: str) -> str:
        pass


if __name__ == "__main__":
    print("=== CODE NEXUS - DATA PROCESSOR FOUNDATION ===\n")
    print("Initializing Numeric Processor...")
    num_p = [1, 2, 3, 4, 5]
    NumericProcessor.process(num_p)
    str_p = "Hello Nexus World"
    log_p = "ERROR: Connection timeout"

