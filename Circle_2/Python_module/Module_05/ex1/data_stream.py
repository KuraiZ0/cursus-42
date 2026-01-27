"""
Module data_stream.

This module implements a polymorphic data stream system capable of handling
sensors, transactions, and events.
"""

from abc import ABC, abstractmethod
from typing import Any, List, Union, Dict, Optional


class DataStream(ABC):
    """Abstract base class for data streams with core functionality."""

    def __init__(self) -> None:
        """Initialize base stream metadata."""
        self.stream_type: str = "Unknown"
        self.data_type: str = "items"

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data and return a summary string."""
        pass

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter data based on optional criteria."""
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return stream statistics."""
        return {}


class SensorStream(DataStream):
    """Specialized stream for environmental sensor data."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the sensor stream."""
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = "Sensor"
        self.data_type = "readings"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process environmental readings (e.g., temperature)."""
        display_batch = ", ".join(
            [f"{k}: {v}" for d in data_batch for k, v in d.items()]
        )
        print(f"Processing sensor batch: [{display_batch}]")

        temps = [d.get("temp", 0) for d in data_batch if "temp" in d]
        if not temps:
            return "No valid temperature data"

        avg = sum(temps) / len(temps)
        return (f"Sensor analysis: {len(data_batch)} readings processed, "
                f"avg temp: {avg}°C")

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter high temperature readings."""
        if criteria == "high":
            return [d for d in data_batch if d.get("temp", 0) > 22.0]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return sensor statistics."""
        return {"id": self.stream_id, "type": "Environmental"}


class TransactionStream(DataStream):
    """Specialized stream for financial transactions."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the transaction stream."""
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = "Transaction"
        self.data_type = "operations"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Calculate net financial flow."""
        formatted = []
        for item in data_batch:
            formatted.extend([f"{k}: {v}" for k, v in item.items()])
        print(f"Processing transaction batch: [{', '.join(formatted)}]")

        net = 0
        for item in data_batch:
            net += item.get("buy", 0)
            net -= item.get("sell", 0)

        sign = "+" if net >= 0 else ""
        return (f"Transaction analysis: {len(data_batch)} operations, "
                f"net flow: {sign}{net} units")

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter large transactions."""
        if criteria == "large":
            return [d for d in data_batch
                    if d.get("buy", 0) > 100 or d.get("sell", 0) > 100]
        return data_batch


class EventStream(DataStream):
    """Specialized stream for system events."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the event stream."""
        super().__init__()
        self.stream_id = stream_id
        self.stream_type = "Event"
        self.data_type = "events"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Analyze events and count errors."""
        print(f"Processing event batch: [{', '.join(data_batch)}]")
        errors = data_batch.count("error")
        return (f"Event analysis: {len(data_batch)} events, "
                f"{errors} error detected")

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str] = None) -> List[Any]:
        """Filter critical error events."""
        if criteria == "critical":
            return [e for e in data_batch if e == "error"]
        return data_batch


class StreamProcessor:
    """Manager that handles multiple stream types polymorphically."""

    def __init__(self) -> None:
        """Initialize the stream list."""
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        """Add a stream to the processor."""
        self.streams.append(stream)

    def process_stream_batch(self, stream_idx: int,
                             data: List[Any]) -> str:
        """Process a batch for a specific stream index."""
        if 0 <= stream_idx < len(self.streams):
            return self.streams[stream_idx].process_batch(data)
        return "Error: Stream index out of range"


if __name__ == "__main__":
    print("CODE NEXUS POLYMORPHIC STREAM SYSTEM")

    # Test Data
    sensor_data = [
        {'temp': 22.5, 'humidity': 65, 'pressure': 1013},
        {'temp': 23.0}, {'temp': 21.0}
    ]
    trans_data = [{'buy': 100}, {'sell': 150}, {'buy': 75}, {'buy': 200}]
    event_data = ['login', 'error', 'logout']

    # Initialization
    processor = StreamProcessor()

    print("\nInitializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")
    sensor.process_batch([sensor_data[0]])
    processor.add_stream(sensor)

    print("\nInitializing Transaction Stream...")
    trans = TransactionStream("TRANS_001")
    print(f"Stream ID: {trans.stream_id}, Type: Financial Data")
    trans.process_batch(trans_data[:3])
    processor.add_stream(trans)

    print("\nInitializing Event Stream...")
    event = EventStream("EVENT_001")
    print(f"Stream ID: {event.stream_id}, Type: System Events")
    event.process_batch(event_data)
    processor.add_stream(event)

    print("\n=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")

    print("\nBatch 1 Results:")
    res1 = processor.process_stream_batch(0, sensor_data[:2])
    print(f"Sensor data: {res1.split(':')[1].strip().split(',')[0]}")

    res2 = processor.process_stream_batch(1, trans_data)
    print(f"Transaction data: {res2.split(':')[1].strip().split(',')[0]}")

    res3 = processor.process_stream_batch(2, event_data)
    print(f"Event data: {res3.split(':')[1].strip().split(',')[0]}")

    print("\nStream filtering active: High-priority data only")
    crit_events = event.filter_data(event_data, "critical")
    large_trans = trans.filter_data(trans_data, "large")
    print(f"Filtered results: {len(crit_events)} critical sensor alerts, "
          f"{len(large_trans)} large transaction")

    print("\nAll streams processed successfully. Nexus throughput optimal.")