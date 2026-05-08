import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["latihan6"]
collection = db["maintenance"]

# Membaca maintenance.csv [cite: 702]
df = pd.read_csv("maintenance.csv")
df['tanggal'] = pd.to_datetime(df['tanggal'])
data_insert = df.to_dict("records")

# Menyisipkan ke database latihan6 [cite: 706]
collection.insert_many(data_insert)
client.close()
