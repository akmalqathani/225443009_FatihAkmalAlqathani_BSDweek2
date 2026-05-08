from pymongo import MongoClient
from datetime import datetime, timedelta
import random

NIM = "225443009"
client = MongoClient('mongodb://localhost:27017')
db = client[f'tugas5_{NIM}']
db.inspeksi.drop()
db.target_kualitas.drop()

mesin_list = [f"M{i:02d}" for i in range(1, 11)]
batch_ids = [f"B{str(i).zfill(4)}" for i in range(1, 2001)]
inspektor_list = ["Andi", "Budi", "Citra", "Dian", "Eka"]
jenis_cacat_options = ["gores", "retak", "bengkok", "warna", "dimensi", "pori"]

docs = []
start_date = datetime(2026, 4, 1, 6, 0)
for i in range(1500):
    tanggal = start_date + timedelta(minutes=random.randint(0, 60*24*90))
    doc = {
        "batch_id": random.choice(batch_ids),
        "mesin": random.choice(mesin_list),
        "tanggal": tanggal,
        "shift": 1 if tanggal.hour < 14 else (2 if tanggal.hour < 22 else 3),
        "inspektor": random.choice(inspektor_list),
        "jumlah_diperiksa": random.randint(100, 500),
        "cacat_ditemukan": int(random.randint(100, 500) * random.uniform(0, 0.10)),
        "jenis_cacat": random.sample(jenis_cacat_options, k=random.randint(1, 3))
    }
    docs.append(doc)
    if len(docs) >= 500:
        db.inspeksi.insert_many(docs)
        docs.clear()
if docs: db.inspeksi.insert_many(docs)

targets = []
for i in range(1, 2001):
    targets.append({"batch_id": f"B{str(i).zfill(4)}", "target_maks_cacat": random.randint(1, 15)})
    if len(targets) >= 500:
        db.target_kualitas.insert_many(targets)
        targets.clear()
if targets: db.target_kualitas.insert_many(targets) 