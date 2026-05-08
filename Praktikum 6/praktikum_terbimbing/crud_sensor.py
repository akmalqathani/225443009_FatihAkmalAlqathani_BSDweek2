import os
import random
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]
collection = db["sensor"]

# 1. Create (Insert Many)
data = []
for i in range(10):
    doc = {
        "mesin": f"CNC-{random.randint(1,3):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.utcnow() - timedelta(minutes=i*5),
        "status": "normal"
    }
    data.append(doc)
collection.insert_many(data)

# 2. Read (Query CNC-01 terbaru)
cursor = collection.find(
    {"mesin": "CNC-01"},
    {"_id": 0, "suhu": 1, "timestamp": 1}
).sort("timestamp", -1).limit(5)

# 3. Update (Status Maintenance jika suhu > 90)
collection.update_many({"suhu": {"$gt": 90}}, {"$set": {"status": "maintenance"}})

# 4. Delete (Data > 1 jam)
satu_jam_lalu = datetime.utcnow() - timedelta(hours=1)
collection.delete_many({"timestamp": {"$lt": satu_jam_lalu}})

client.close()
