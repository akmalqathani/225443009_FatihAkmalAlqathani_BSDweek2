import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
# Koneksi MongoDB menggunakan URI dari environment variable
client = MongoClient(os.getenv("MONGO_URI"), serverSelectionTimeoutMS=5000)

try:
    client.admin.command('ping')
    print("Koneksi MongoDB berhasil!")
except Exception as e:
    print("Gagal terhubung:", e)
finally:
    client.close()
    