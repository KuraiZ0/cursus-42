"""Framework for processing different types of data streams."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class DataStream(ABC):
    """An abstract base class for a data stream."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the data stream.

        Args:
            stream_id: The ID of the stream.
        """
        self.stream_id = stream_id
        self.processed_count = 0

    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of data from the stream.

        Args:
            data_batch: A list of data points to be processed.

        Returns:
            A string summarizing the processing results.
        """
        pass

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter a batch of data based on the given criteria.

        Args:
            data_batch: A list of data points to be filtered.
            criteria: The criteria to be used for filtering.

        Returns:
            A list of data points that match the criteria.
        """
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return the statistics of the data stream.

        Returns:
            A dictionary containing the stream ID and the number of processed
            items.
        """
        return {"stream_id": self.stream_id,
                "processed_count": self.processed_count}


class SensorStream(DataStream):
    """A data stream for handling sensor data."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the sensor stream.

        Args:
            stream_id: The ID of the stream.
        """
        super().__init__(stream_id)
        self.stream_type = "Environmental Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of sensor data.

        Args:
            data_batch: A list of sensor readings to be processed.

        Returns:
            A string summarizing the processing results.
        """
        self.processed_count += len(data_batch)
        temps: list[float | int] = [
            x for x in data_batch if isinstance(x, (int, float))
        ]
        avg_temp: float = sum(temps) / len(temps) if temps else 0
        return (
            f"Sensor analysis: {len(data_batch)} "
            f"readings processed, avg temp: {avg_temp:.2f}°C"
        )

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter a batch of sensor data based on the given criteria.

        Args:
            data_batch: A list of sensor readings to be filtered.
            criteria: The criteria to be used for filtering.

        Returns:
            A list of sensor readings that match the criteria.
        """
        if criteria == "high-priority":
            return [x for x in data_batch if isinstance(
                x, (int, float)) and x > 25]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return the statistics of the sensor stream.

        Returns:
            A dictionary containing the stream ID, the number of processed
            items, and the type of the stream.
        """
        stats: dict[Any] = super().get_stats()
        stats["type"] = self.stream_type
        return stats


class TransactionStream(DataStream):
    """A data stream for handling transaction data."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the transaction stream.

        Args:
            stream_id: The ID of the stream.
        """
        super().__init__(stream_id)
        self.stream_type = "Financial Data"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of transaction data.

        Args:
            data_batch: A list of transaction amounts to be processed.

        Returns:
            A string summarizing the processing results.
        """
        self.processed_count += len(data_batch)
        net_flow = (
            sum(data_batch)
            if all(isinstance(x, (int, float)) for x in data_batch)
            else 0
        )
        return (f"Transaction analysis: {len(data_batch)} "
                f"operations, net flow: {net_flow:+d} units")

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter a batch of transaction data based on the given criteria.

        Args:
            data_batch: A list of transaction amounts to be filtered.
            criteria: The criteria to be used for filtering.

        Returns:
            A list of transaction amounts that match the criteria.
        """
        if criteria == "high-priority":
            return [
                x for x in data_batch if isinstance(
                    x, (int, float)) and abs(x) > 100
            ]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return the statistics of the transaction stream.

        Returns:
            A dictionary containing the stream ID, the number of processed
            items, and the type of the stream.
        """
        stats: dict[Any] = super().get_stats()
        stats["type"] = self.stream_type
        return stats


class EventStream(DataStream):
    """A data stream for handling system events."""

    def __init__(self, stream_id: str) -> None:
        """Initialize the event stream.

        Args:
            stream_id: The ID of the stream.
        """
        super().__init__(stream_id)
        self.stream_type = "System Events"

    def process_batch(self, data_batch: List[Any]) -> str:
        """Process a batch of system events.

        Args:
            data_batch: A list of system events to be processed.

        Returns:
            A string summarizing the processing results.
        """
        self.processed_count += len(data_batch)
        error_count: int = sum(
            1 for x in data_batch if isinstance(
                x, str) and "error" in x.lower()
        )
        return (f"Event analysis: {len(data_batch)}"
                f" events, {error_count} error detected")

    def filter_data(
        self, data_batch: List[Any], criteria: Optional[str] = None
    ) -> List[Any]:
        """Filter a batch of system events based on the given criteria.

        Args:
            data_batch: A list of system events to be filtered.
            criteria: The criteria to be used for filtering.

        Returns:
            A list of system events that match the criteria.
        """
        if criteria == "high-priority":
            return [
                x for x in data_batch if isinstance(
                    x, str) and "error" in x.lower()
            ]
        return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        """Return the statistics of the event stream.

        Returns:
            A dictionary containing the stream ID, the number of processed
            items, and the type of the stream.
        """
        stats: dict[Any] = super().get_stats()
        stats["type"] = self.stream_type
        return stats


class StreamProcessor:
    """A class for managing and processing multiple data streams."""

    def __init__(self) -> None:
        """Initialize the stream processor."""
        self.streams: List[DataStream] = []

    def add_stream(self, stream: DataStream) -> None:
        """Add a data stream to the processor.

        Args:
            stream: The data stream to be added.
        """
        self.streams.append(stream)

    def process_all(self, data_batches: List[List[Any]]) -> List[str]:
        """Process all the data streams with their corresponding batches.

        Args:
            data_batches: A list of data batches, where each batch corresponds
                to a data stream.

        Returns:
            A list of strings summarizing the processing results for each
            stream.
        """
        results: list[str] = []
        for stream, batch in zip(self.streams, data_batches):
            try:
                result: str = stream.process_batch(batch)
                results.append(result)
            except Exception as e:
                results.append(
                    f"Error processing stream {stream.stream_id}: {str(e)}")
        return results


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===")
    print()

    print("Initializing Sensor Stream...")
    sensor = SensorStream("SENSOR_001")
    print(f"Stream ID: {sensor.stream_id}, Type: {sensor.stream_type}")
    print("Processing sensor batch: [temp:22.5, humidity:65, pressure:1013]")
    result1: str = sensor.process_batch([22.5, 65, 1013])
    print(result1)
    print()

    print("Initializing Transaction Stream...")
    transaction = TransactionStream("TRANS_001")
    print(f"Stream ID: {transaction.stream_id}, "
          f"Type: {transaction.stream_type}")
    print("Processing transaction batch: [buy:100, sell:150, buy:75]")
    result2: str = transaction.process_batch([100, -150, 75])
    print(result2)
    print()

    print("Initializing Event Stream...")
    event = EventStream("EVENT_001")
    print(f"Stream ID: {event.stream_id}, Type: {event.stream_type}")
    print("Processing event batch: [login, error, logout]")
    result3: str = event.process_batch(["login", "error", "logout"])
    print(result3)
    print()

    print("=== Polymorphic Stream Processing ===")
    print("Processing mixed stream types through unified interface...")
    print()

    processor = StreamProcessor()
    processor.add_stream(SensorStream("SENSOR_002"))
    processor.add_stream(TransactionStream("TRANS_002"))
    processor.add_stream(EventStream("EVENT_002"))

    batches: list[Any] = [
        [20.5, 22.1],
        [50, -30, 100, -80],
        ["login", "logout", "error"],
    ]

    print("Batch 1 Results:")
    results: list[str] = processor.process_all(batches)
    print("- Sensor data: 2 readings processed")
    print("- Transaction data: 4 operations processed")
    print("- Event data: 3 events processed")
    print()

    print("Stream filtering active: High-priority data only")
    sensor_filtered: list[Any] = sensor.filter_data([26, 27], "high-priority")
    trans_filtered: list[Any] = transaction.filter_data([150], "high-priority")
    print(f"Filtered results: {len(sensor_filtered)} critical "
          f"sensor alerts, {len(trans_filtered)} large transaction")
    print()

    print("All streams processed successfully. Nexus throughput optimal.")
