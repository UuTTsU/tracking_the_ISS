import requests
import time
import json
import asyncio

class Collection:
    def __init__(self, url, file_path):
        self.url = url
        self.file_path = file_path

    async def data_lake(self):
        while True:
            response = requests.get(self.url)
            json_data_api = json.dumps(response.json(), indent=4)
            with open(self.file_path) as json_data_file:
                data = json.load(json_data_file)

            data["Satellite Positions"].append(json_data_api)
            with open(self.file_path, "w") as json_data_file:
                json.dump(data, json_data_file, indent=4)

            await asyncio.sleep(5)
