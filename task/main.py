from model.meter import Meter
from model.reading import Reading
from db.sqlite import SqliteDb
import json
from typing import List
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

if __name__ == "__main__":
    with open("resources/meters.json") as fh:
        meters: List[Meter] = json.load(fh)

    print(f"Loaded {len(meters)} meters")
    print(meters)

    db = SqliteDb("resources/sqlite.db")
    meters_map = {}
    for meter_dict in meters:
        meter = Meter.from_dict(meter_dict)
        db.store_meter(meter)
        meters_map[meter.serial_number] = meter

    readings_csv = pd.read_csv("resources/readings.csv")
    readings = []
    for _, row in readings_csv.iterrows():
        serial_num = row["Serial Number"]
        meter = meters_map[serial_num]
        value = meter.normalise_reading(row["Reading"])
        reading = Reading(
                serial_number = serial_num,
                datetime = row["Time"],
                value = value
            )
        readings.append(reading)
    db.store_readings(readings)

    power = db.power()

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator())
    plt.plot(
        [dt.datetime.strptime(p.datetime,'%Y-%m-%d %H:%M:%S') for p in power], 
        [p.value for p in power], 
        )

    plt.xlabel("Time")
    plt.ylabel("Power (W)")
    plt.gcf().autofmt_xdate()
    plt.show()

    HOURS_PER_MEASUREMENT = 1/60
    total_energy = sum([p.value * HOURS_PER_MEASUREMENT / 1_000 for p in power])
    print(f"Total energy consumption (kWh): {total_energy}")

    




