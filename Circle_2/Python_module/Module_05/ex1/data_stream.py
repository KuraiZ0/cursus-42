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
    def __init__(self):
        self.stream_type: str = "Unknow"
        self.data_type: str = "items"

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        result: Dict = {}
        return result


class SensorStream(DataStream):
    """Abstract base class for sensor streams."""
    def __init__(self, stream_id: str):
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = "Sensor"
        self.data_type = "readings"

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
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter data batch."""
        if criteria == "high":
            result: List[Any] = (
                [item for item in data_batch if item["temp"] > 20])
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
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = "Transaction"
        self.data_type = "operations"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process transaction batch."""
        print(f"Processing transaction batch: [{data_batch}]")
        buy: List[Any] = [item["buy"] for item in data_batch if "buy" in item]
        sell: List[Any] = (
            [item["sell"] for item in data_batch if "sell" in item])
        units: int = sum(buy) - sum(sell)
        sign: str = "+" if units >= 0 else ""
        result: str = (
            f"Transaction analysis: {len(data_batch)} operations, "
            f"net flow: {sign}{units} units")
        return result

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """"Filter transaction batch."""
        if criteria == "buy":
            result_buy: List[Any] = (
                [item for item in data_batch if item["buy"]])
            return result_buy
        elif criteria == "sell":
            result_sell: List[Any] = (
                [item for item in data_batch if item["sell"]])
            return result_sell
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
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = "Event"
        self.data_type = "events"

    def process_batch(self, data_batch: List[Any]) -> str:
        """"Process event batch."""
        print(f"Processing event batch: [{data_batch}]")
        length = len(data_batch)
        # login: List[Any] = [item for item in data_batch if item["login"]]
        error: List[Any] = [item for item in data_batch if item == "error"]
        len_error: int = len(error)
        # logout: List[Any] = [item for item in data_batch if item["logout"]]
        result: str = (
            f"Event analysis: {length} events, {len_error} error detected")
        return result

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """"Filter event batch."""
        if criteria == "error":
            return (data_batch)
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
        print("Processing mixed stream types through unified interface...\n")

        for index, stream in enumerate(self.streams):
            result = stream.process_batch(data_batch[index])
            results.append(
                f"{stream.stream_type} data: {len(data_batch[index])} "
                f"{stream.data_type} processed")

        printable = "Batch 1 Results:\n"
        for result in results:
            printable += f"- {result}\n"
        return printable


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")

    sensor = SensorStream("SENSOR_001")
    sensor_data: Dict[str, float] = {
        'temp': 22.5,
        'humidity': 65,
        'pressure': 1013,
    }
    trans = TransactionStream("TRANS_001")
    trans_data: List[Dict[str, int]] = [
        {'buy': 412},
        {'sell': 1342},
        {'buy': 134}
    ]
    event = EventStream("EVENT_001")
    event_data: List[str] = [
        'login',
        'error',
        'logout'
    ]
    stream = StreamProcessor()
    stream.add_stream(sensor)
    stream.add_stream(trans)
    stream.add_stream(event)

    print("Initializing Sensor Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")
    sensor.process_batch([sensor_data])
    print()
    print("Initializing Transaction Stream...")
    print(f"Stream ID: {trans.stream_id}, Type: Financial Data")
    trans.process_batch(trans_data)
    print()
    print("Initializing Event Stream...")
    print(f"Stream ID: {event.stream_id}, Type: System Events")
    event.process_batch(event_data)
    print()
    print("=== Polymorphic Stream Processing ===")
    print(stream.process_all([
        [sensor_data],
        trans_data,
        event_data]))
    print()
    print("Stream filtering active: High-priority data only")
    print("Filtered results: {crit_err} critical sensor alerts, "
          "{larg_trans} large transaction")
    print()
    print("All streams processed successfully. Nexus throughput optimal.")
