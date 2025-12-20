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
from typing import Any, List, Union, Dict


class DataStream(ABC):    
    @abstractmethod
    def process_batch(self, data_batch: List[Any]) -> str:
        pass
    
    def filter_data(self, data_batch: List[Any],
    criteria: Optional[str]=None) -> List[Any]:
        pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass


class SensorStream(DataStream):
    def __init__(self, stream_id: str):
        self.stream_id = stream_id

    def process_batch(self, data_batch: List[Any]) -> str:
        print(f"Processing sensor batch: {data_batch}")
        rd_proc = len(data_batch)

        temp = [item["temp"] for item in data_batch]
        avg = sum(temp) / len(temp)
        result = (f"Sensor analysis: {rd_proc}, avg temp: {avg}")

        print(result)
        return result

    def filter_data(self, data_batch: List[Any],
                    criteria: Optional[str]=None) -> List[Any]:
        
        if criteria == None:
            return data_batch
        elif criteria == "high":
            result = [item for item in data_batch if item["temp"] > 20]
            return result
        else:
            return data_batch

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass

class TransactionStream(DataStream):
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
    def process_batch(self, data_batch: List[Any]) -> str:
        pass

    def filter_data(self, data_batch: List[Any],
    criteria: Optional[str]=None) -> List[Any]:
    pass

    def get_stats(self) -> Dict[str, Union[str, int, float]]:
        pass

class EventStream(DataStream):
    def __init__(self, stream_id: str):
        self.stream_id = stream_id
    def process_batch(self, data_batch: List[Any]) -> str:

    def filter_data(self, data_batch: List[Any],
    criteria: Optional[str]=None) -> List[Any]:

    def get_stats(self) -> Dict[str, Union[str, int, float]]:

class StreamProcessor(DataStream):
    def process_batch(self, data_batch: List[Any]) -> str:


if __name__ == "__main__":
    print("=== CODE NEXUS - POLYMORPHIC STREAM SYSTEM ===\n")
    
    sensor = SensorStream("SENSOR_001")
    trans = TransactionStream("TRANS_001")
    event = EventStream("EVENT_001")

    print("Initializing Sensor Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Environmental Data")

    print("Initializing Transaction Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: Financial Data")


    print("Initializing Event Stream...")
    print(f"Stream ID: {sensor.stream_id}, Type: System Events")
