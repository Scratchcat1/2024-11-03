from dataclasses import dataclass
from typing import Dict, Self

@dataclass
class Meter:
    service_date: str
    building_area: str
    service: str
    serial_number: str
    unit: str

    @staticmethod
    def from_dict(d: Dict[str, str]) -> Self:
        return Meter(
            serial_number = d["serial_number"],
            building_area = d["building_area"],
            service = d["service"],
            service_date = d["service_date"],
            unit = d["unit"],
        )

    def normalise_reading(self, measurement: float) -> float:
        if self.unit == "kW":
            return measurement * 1000
        else:
            raise Exception("Unexpected unit")