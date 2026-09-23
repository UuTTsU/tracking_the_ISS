import os
from dotenv import load_dotenv
from collection import Collection
from storage import Storage
import psycopg2
from transformation import Transformation


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
print(t1)

# c1.data_lake()
# s1.store_to_db()






