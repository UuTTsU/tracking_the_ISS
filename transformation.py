from opencage.geocoder import OpenCageGeocode
from pprint import pprint

class Transformation:
    def __init__(self, db_conn, geocode_api):
        self.__db_conn = db_conn
        self.__geocode_api = geocode_api

    def where_is_iss(self):
        cur = self.__db_conn.cursor()

        cur.execute("""
                    select longtitude, latitude
                    from ISS_Record
                    order by timestamp_iss desc limit 1

                    """)
        coordinates = cur.fetchall()
        longitude = coordinates[0][0]
        latitude = coordinates[0][1]
        geocoder = OpenCageGeocode(self.__geocode_api)
        result = geocoder.reverse_geocode(latitude, longitude)
        return result[0]["formatted"]

    def distance_iss(self):
        cur = self.__db_conn.cursor()
        cur.execute("""
               SELECT
               recordID,
               timestamp_iss,
               velocity,
               timestamp_iss - LAG(timestamp_iss) OVER (ORDER BY timestamp_iss) AS elapsed_seconds,
               velocity * (timestamp_iss - LAG(timestamp_iss) OVER (ORDER BY timestamp_iss)) / 3600.0 AS distance_km
               FROM ISS_Record
               ORDER BY timestamp_iss desc limit 1
        """)
        distances = cur.fetchall()
        values = (distances[0][0],distances[0][3],distances[0][4])
        cur.execute("""

                    INSERT INTO ISS_Info (recordid, distance, whereIsIt)
                    VALUES (%s, %s, %s) on conflict (recordid) do nothing
                    """, values)

        self.__db_conn.commit()
        return distances[0][4]

    def __str__(self) -> str:
        return (f"Currently satelite is above {self.where_is_iss()} "
                f"it has moved {self.distance_iss()} km from the last position")



