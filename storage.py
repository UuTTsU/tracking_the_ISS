import ast
import json
import time
class Storage:
    def __init__(self, db_conn, file_path):
        self.db_conn = db_conn
        self.file_path = file_path

    def store_to_db(self):
        while True:
            cur = self.db_conn.cursor()
            with (open(self.file_path) as f):
                data = json.load(f)
                for value in data["Satellite Positions"]:
                    i = ast.literal_eval(value)

                    values = (i["name"], i["id"], i["latitude"], i["longitude"], i["altitude"], i["velocity"],
                              i["visibility"], i["footprint"], i["timestamp"], i["daynum"], i["solar_lat"],
                              i["solar_lon"], i["units"])
                    cur.execute("""
                    
                                INSERT INTO ISS_Record (Satellite_name, satelliteID, latitude, longtitude, altitude,
                                                        velocity,
                                                        visibility, footprint, timestamp_iss, daynum, solar_lat,
                                                        solar_lon, units)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                on conflict (timestamp_iss) do nothing
                                """, values)

                    self.db_conn.commit()
            time.sleep(5)
