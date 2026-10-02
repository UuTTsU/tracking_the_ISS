"""
This module handles transforming raw ISS coordinate data into readable locations 
and calculating the distance traveled between database entries.
"""

from opencage.geocoder import OpenCageGeocode
import asyncio
from logger_config import setup_logger

logger = setup_logger(__name__)


class Transformation:
    """
    A class to perform reverse geocoding on ISS coordinates and calculate 
    its travel distance based on database records.

    Attributes:
        __db_conn: The active database connection object.
        __geocode_api (str): The API key for the OpenCage Geocoding service.
    """

    def __init__(self, db_conn, geocode_api):
        """
        Initializes the Transformation object.

        Args:
            db_conn: The active database connection object.
            geocode_api (str): The OpenCage API key.
        """
        self.__db_conn = db_conn
        self.__geocode_api = geocode_api

    async def where_is_iss(self):
        """
        Retrieves the most recent ISS coordinates from the database and performs 
        a reverse geocode to find its human-readable location.

        Returns:
            str: A formatted address/location string where the ISS is currently flying over.
        """
        cur = self.__db_conn.cursor()

        # Fetch the latest latitude and longitude
        cur.execute("""
                    SELECT longtitude, latitude
                    FROM ISS_Record
                    ORDER BY timestamp_iss DESC LIMIT 1
                    """)
        coordinates = cur.fetchall()
        longitude = coordinates[0][0]
        latitude = coordinates[0][1]

        # Reverse geocode the coordinates
        geocoder = OpenCageGeocode(self.__geocode_api)
        result = geocoder.reverse_geocode(latitude, longitude)

        return result[0]["formatted"]

    async def distance_iss(self):
        """
        Calculates the distance the ISS has traveled since the previous record.

        It calculates the elapsed time using SQL window functions (LAG) and multiplies 
        it by the velocity to get the distance in kilometers. It also fetches the current 
        human-readable location and stores this combined data into the ISS_Info table.

        Returns:
            tuple: A tuple containing the current location (str) and the distance traveled (float).
        """
        cur = self.__db_conn.cursor()

        # Calculate elapsed time and distance using the previous database record
        cur.execute("""
                    SELECT recordID,
                           timestamp_iss,
                           velocity,
                           timestamp_iss - LAG(timestamp_iss) OVER (ORDER BY timestamp_iss) AS elapsed_seconds, velocity * (timestamp_iss - LAG(timestamp_iss) OVER (ORDER BY timestamp_iss)) / 3600.0 AS distance_km
                    FROM ISS_Record
                    ORDER BY timestamp_iss DESC LIMIT 1
                    """)
        distances = cur.fetchall()

        # Get the human-readable location
        location = await self.where_is_iss()

        # Insert the transformed data into the ISS_Info table
        values = (distances[0][0], distances[0][3], location)
        cur.execute("""
                    INSERT INTO ISS_Info (recordid, distance, whereIsIt)
                    VALUES (%s, %s, %s) ON CONFLICT (recordid) DO NOTHING
                    """, values)

        self.__db_conn.commit()

        # distances[0][4] is the calculated distance_km
        return location, distances[0][4]

    async def run(self):
        """
        Continuously calculates distance and location, logging the results.

        This method runs asynchronously in an infinite loop. Every 10 seconds, it triggers 
        the distance and location calculations and logs the output to the console.
        """
        while True:
            location, distance = await self.distance_iss()
            logger.info(f"ISS has moved {distance} km from the last position, currently it is at {location}")

            await asyncio.sleep(10)