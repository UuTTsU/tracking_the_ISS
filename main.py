import os
from dotenv import load_dotenv
from collection import Collection
from storage import Storage
import psycopg2
from transformation import Transformation
import asyncio
from logger_config import setup_logger
logger = setup_logger(__name__)


load_dotenv()
geocode_api_key = os.getenv("GEOCODE_API_KEY")
db_url = os.getenv("DATABASE_URL")
is_debug = os.getenv("DEBUG")=="True"
iss_api_url = os.getenv("ISS_API_URL")

conn=psycopg2.connect(db_url)

data_collector = Collection(iss_api_url, "data.json")
data_storage= Storage(conn,"data.json")
data_transformer = Transformation(conn, geocode_api_key)


async def main():
    conc = await asyncio.gather(
        data_collector.data_lake(),
        data_storage.store_to_db(),
        data_transformer.run()

    )

try:
    while True:
        asyncio.run(main())
except KeyboardInterrupt as k:
    logger.error(f'the programme was stopped by admin {k}')

# c1.data_lake()
# s1.store_to_db()




