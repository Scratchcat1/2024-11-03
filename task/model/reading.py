from dataclasses import dataclass

@dataclass
class Reading:
    serial_number: str
    datetime: str
    value: float