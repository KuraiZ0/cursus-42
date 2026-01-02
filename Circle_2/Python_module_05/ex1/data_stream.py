# ****************************************************************************#
#                                                                             #
#                                                         :::      ::::::::   #
#    data_stream.py                                     :+:      :+:    :+:   #
#                                                     +:+ +:+         +:+     #
#    By: ialmani <ialmani@student.42belgium.be>     +#+  +:+       +#+        #
#                                                 +#+#+#+#+#+   +#+           #
#    Created: 2025/12/20 19:21:56 by ialmani           #+#    #+#             #
#    Updated: 2025/12/20 19:21:56 by ialmani          ###   ########.fr       #
#                                                                             #
# ****************************************************************************#
from abc import ABC, abstractmethod
from typing import Any, List, Union, Dict, Optional


class DataStream(ABC):
    """Abstract base class for data streams."""
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass
    
    def filter_data(self, data_batch: List[Any],
    criteria: Optional[str]=None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    """Abstract base class for sensor streams."""
    def __init__(self, stream_id: str):
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process sensor batch."""
        print(f"Processing sensor batch: [{data_batch}]")
        len_data: int = len(data_batch)

        temp: List[Any] = [item["temp"] for item in data_batch]
        avg: float = sum(temp) / len(temp)
        result: str = (f"Sensor analysis: {len_data} readings processed"
                       f", avg temp: {avg}°C")

        print(result)
        return result

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str]=None) -> List[Any]:
        """Filter data batch."""
        if criteria == "high":
            result: List[Any] = [item for item in data_batch if item["temp"] > 20]
            return result
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Get sensor stats."""
        return {
            "status": "active",
            "avg_temp": 18.3,
            "max_temp": 22.5
        }

class TransactionStream(DataStream):
    """Abstract base class for transaction streams."""
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction batch."""
        print(f"Processing transaction batch: [{data_batch}]")
        buy: List[Any] = [item["buy"] for item in data_batch if "buy" in item]
        sell: List[Any] = [item["sell"] for item in data_batch if "sell" in item]
        units: int = sum(buy) - sum(sell)
        sign: str = "+" if units >= 0 else ""
        result: str = f"Transaction analysis: {len(data_batch)} operations, net flow: {sign}{units} units"
        return result

    def filter_data(self, data_batch: List[Any],
    criteria: Optional[str]=None) -> List[Any]:
        """"Filter transaction batch."""
        if criteria == "buy":
            result: List[Any] = [item for item in data_batch if item["buy"]]
            return result
        elif criteria == "sell":
            result: List[Any] = [item for item in data_batch if item["sell"]]
            return result
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Get transaction stats."""
        return {
            "stream_id": self.stream_id,
            "status": "active",
            "max_buy": 22.5,
            "net_flow": 25
        }

class EventStream(DataStream):
    """Abstract base class for event streams."""
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
    def process_batch(self, data_batch: List[Any]) -> str:
        """"Process event batch."""
        print(f"Processing event batch: [{data_batch}]")
        length = len(data_batch)
        # login: List[Any] = [item for item in data_batch if item["login"]]
        error: List[Any] = [item for item in data_batch if item == "error"]
        len_error: int = len(error)
        # logout: List[Any] = [item for item in data_batch if item["logout"]]
        result: str = f"Event analysis: {length} events, {len_error} error detected"
        return result

    def filter_data(self, data_batch: List[Any],
    criteria: Optional[str]=None) -> List[Any]:
        """"Filter event batch."""
        if criteria == "error":
            return "An error occured!"
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Get event stats."""
        return {
            "stream_id": self.stream_id,
            "status": "active",
            "avg_error": 18.3,
        }


class StreamProcessor:
    """Manager that handles multiple stream types polymorphically."""
    def __init__(self):
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream):
        """Add stream to the processor."""
        self.streams.append(stream)

    def process_all(self, data_batch: List[Any]) -> str:
        """Process all data through polymorphically."""
        results: List[str] = []

        for index, stream in enumerate(self.streams):
            result = stream.process_batch(data_batch[index])
            results.append(result)
        return results


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    
    sensor = SensorStream("SENSOR_001")
    sensor_data: Dict[str, float] = {
        'temp': 22.5,
        'humidity': 65,
        'pressure': 1013,
    }
    trans = TransactionStream("TRANS_001")
    event = EventStream("EVENT_001")

    print("Initializing Sensor Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")
    sensor.process_batch([sensor_data])
    print()
    print("Initializing Transaction Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Financial Data")


    print("Initializing Event Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: System Events")
