import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["latihan6"]
collection = db["maintenance"]

print("\n A. DATA DENGAN BIAYA DI ATAS Rp 1.000.000 ")
cursor_mahal = collection.find({"biaya": {"$gt": 1000000}}, {"_id": 0})

df_mahal = pd.DataFrame(list(cursor_mahal))
print(df_mahal)

print("\nB. PROSES UPDATE DATA TEKNISI ")
update_result = collection.update_one(
    {"mesin": "CNC-01", "biaya": 1200000},
    {"$set": {"teknisi": "Dewi"}}    
)
print(f"Jumlah data yang berhasil di-update: {update_result.modified_count} dokumen.")

print("\nC. REKAP TOTAL BIAYA MAINTENANCE PER BULAN ")
pipeline = [
    {
        "$group": {
            "_id": { "$dateToString": { "format": "%Y-%m", "date": "$tanggal" } },
            "total_biaya": { "$sum": "$biaya" }
        }
    },
    { 
        "$sort": { "_id": 1 } 
    }
]

hasil_agregasi = collection.aggregate(pipeline)
df_agregasi = pd.DataFrame(list(hasil_agregasi))

df_agregasi.rename(columns={"_id": "Bulan", "total_biaya": "Total Biaya (Rp)"}, inplace=True)
print(df_agregasi)
