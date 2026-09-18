import os
from dotenv import load_dotenv
from collection import Collection

load_dotenv()
geocode_api_key = os.getenv("GEOCODE_API_KEY")
db_url = os.getenv("DATABASE_URL")
is_debug = os.getenv("DEBUG")=="True"
iss_api_url = os.getenv("ISS_API_URL")

c1 = Collection(iss_api_url, "data.json")
c1.data_lake()

