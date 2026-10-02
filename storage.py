"""
This module handles reading satellite data from a local JSON file 
and storing it securely into a PostgreSQL database.
"""

import json
import asyncio


class Storage:
    """
    A class to manage the transfer of satellite position data from a local JSON file 
    to a relational database.

    Attributes:
        db_conn: The active database connection object (e.g., psycopg2 connection).
        file_path (str): The path to the local JSON file to read data from.
    """

    def __init__(self, db_conn, file_path):
        """
        Initializes the Storage object.

        Args:
            db_conn: The active database connection object.
            file_path (str): The path to the JSON file containing satellite data.
        """
        self.db_conn = db_conn
        self.file_path = file_path

    async def store_to_db(self):
        """
        Continuously reads data from the JSON file and inserts it into the database.

        This method runs asynchronously in an infinite loop. Every 5 seconds, it opens 
        the local JSON file, extracts the list of satellite positions, and inserts any 
        new records into the ISS_Record table. It uses a conflict resolution strategy 
        (ON CONFLICT DO NOTHING) to prevent duplicate entries based on the timestamp.
        """
        while True:
            cur = self.db_conn.cursor()

            # Read the parsed data from the JSON file
            with open(self.file_path) as f:
                data = json.load(f)

                # Loop through each position and insert it into the database
                for value in data["Satellite Positions"]:
                    i = value

                    values = (
                        i["name"], i["id"], i["latitude"], i["longitude"],
                        i["altitude"], i["velocity"], i["visibility"],
                        i["footprint"], i["timestamp"], i["daynum"],
                        i["solar_lat"], i["solar_lon"], i["units"]
                    )

                    cur.execute("""
                                INSERT INTO ISS_Record (Satellite_name, satelliteID, latitude, longtitude, altitude,
                                                        velocity, visibility, footprint, timestamp_iss, daynum,
                                                        solar_lat,
                                                        solar_lon, units)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                                        %s) ON CONFLICT (timestamp_iss) DO NOTHING
                                """, values)

                    self.db_conn.commit()

            # Wait 5 seconds before checking the file again
            await asyncio.sleep(5)