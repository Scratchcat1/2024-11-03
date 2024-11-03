from dataclasses import dataclass

@dataclass
class TimedReading:
    datetime: str
    value: float