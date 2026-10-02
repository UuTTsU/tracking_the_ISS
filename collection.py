"""
This module handles the continuous collection of data from an API
and stores the results in a local JSON file.
"""

import requests
import time
import json
import asyncio


class Collection:
    """
    A class to collect data from a specified API and append it to a local JSON file.

    Attributes:
        url (str): The API endpoint to fetch data from.
        file_path (str): The path to the local JSON file where data is stored.
    """

    def __init__(self, url, file_path):
        """
        Initializes the Collection object.

        Args:
            url (str): The URL of the API to pull data from.
            file_path (str): The path to the JSON file to update.
        """
        self.url = url
        self.file_path = file_path

    async def data_lake(self):
        """
        Continuously fetches data from the API and appends it to the JSON file.

        This method runs asynchronously in an infinite loop. Every 5 seconds,
        it sends a GET request to the API, parses the JSON response, reads the
        existing data from the local file, appends the new data, and rewrites
        the file.
        """
        while True:
            # Fetch the data from the API
            response = requests.get(self.url)

            # Parse the API response into a Python dictionary
            json_data_api = response.json()

            # Read the existing data from the local JSON file
            with open(self.file_path) as json_data_file:
                data = json.load(json_data_file)

            # Append the new dictionary to the list
            data["Satellite Positions"].append(json_data_api)

            # Save the updated data back to the JSON file
            with open(self.file_path, "w") as json_data_file:
                json.dump(data, json_data_file, indent=4)

            # Wait 5 seconds before fetching again
            await asyncio.sleep(5)


