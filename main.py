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
database = os.getenv("DATABASE"),
user = os.getenv("USER"),
password = os.getenv("PASSWORD"),
host = os.getenv("HOST"),
port = os.getenv("PORT"),

conn = psycopg2.connect(
            database="ISS",
            user="postgres",
            password="Matiashvili1.",
            host="127.0.0.1",
            port=5432,
        )

c1 = Collection(iss_api_url, "data.json")
s1 = Storage(conn,"data.json")
t1 = Transformation(conn, geocode_api_key)


try:
    async def main():

        conc = await asyncio.gather(
            c1.data_lake(),
            s1.store_to_db(),
            t1.run()

        )


    while True:
        asyncio.run(main())
except KeyboardInterrupt as k:
    logger.error(f'the programme was stopped by admin {k}')


logger.info("Reviewing Project. . . ")

# c1.data_lake()
# s1.store_to_db()




