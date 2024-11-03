import sqlite3 as sq
from model.meter import Meter
from model.reading import Reading
from model.timed_reading import TimedReading
from typing import List

class SqliteDb:
    __conn: sq.Connection

    def __init__(self, file_path: str):
        self.__conn = sq.connect(file_path)
        cur = self.__conn.cursor()
        cur.execute("DROP TABLE IF EXISTS meters")
        cur.execute("CREATE TABLE IF NOT EXISTS meters (serial_number TEXT, service TEXT, building_area TEXT, unit TEXT, service_date TEXT)")
        cur.execute("DROP TABLE IF EXISTS readings")
        cur.execute("CREATE TABLE IF NOT EXISTS readings (serial_number TEXT, datetime TEXT, value REAL)")
        self.__conn.commit()
        cur.close()

    def store_meter(self, meter: Meter):
        cur = self.__conn.cursor()
        params = {
            "serial_number": meter.serial_number,
            "service": meter.service,
            "building_area": meter.building_area,
            "unit": meter.unit,
            "service_date": meter.service_date
        }
        cur.execute("INSERT INTO meters values (:serial_number, :service, :building_area,:unit, :service_date)", params)
        self.__conn.commit()
        cur.close()

    def store_readings(self, readings: List[Reading]):
        cur = self.__conn.cursor()
        params = [{
            "serial_number": reading.serial_number,
            "datetime": reading.datetime,
            "value": reading.value,
        } for reading in readings]
        cur.executemany("INSERT INTO readings values (:serial_number, :datetime, :value)", params)
        self.__conn.commit()
        cur.close()

    def power(self) -> List[TimedReading]:
        cur = self.__conn.cursor()
        query = cur.execute("SELECT datetime, SUM(value) AS total_power FROM readings GROUP BY datetime ORDER BY datetime")
        results = [
            TimedReading(row[0], row[1]) for row in query.fetchall()
        ]
        cur.close()
        return results

