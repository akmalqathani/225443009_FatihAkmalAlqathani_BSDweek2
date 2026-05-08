from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient('mongodb://localhost:27017')
db = client['studi_kasus_oee']
collection = db['produksi_harian']
collection.drop()  # Mulai bersih

mesin_list = [f"M{i:02d}" for i in range(1, 11)]
start_date = datetime(2026, 4, 1)
docs = []

for i in range(1000):
    day_offset = random.randint(0, 90)
    tanggal = start_date + timedelta(days=day_offset)
    shift = random.randint(1, 3)
    mesin = random.choice(mesin_list)
    target = random.randint(200, 500)
    actual_ok = int(target * random.uniform(0.6, 1.0))
    actual_reject = int(actual_ok * random.uniform(0, 0.15))
    durasi_tersedia = 480  # 8 jam
    durasi_operasi = int(durasi_tersedia * random.uniform(0.7, 1.0))

    doc = {
        "mesin": mesin,
        "tanggal": tanggal,
        "shift": shift,
        "target": target,
        "actual_ok": actual_ok,
        "actual_reject": actual_reject,
        "durasi_operasi_menit": durasi_operasi,
        "durasi_tersedia_menit": durasi_tersedia
    }
    docs.append(doc)

    if len(docs) >= 500:
        collection.insert_many(docs)
        docs.clear()

if docs:
    collection.insert_many(docs)

print("Data berhasil dibuat. Total:", collection.count_documents({})) 