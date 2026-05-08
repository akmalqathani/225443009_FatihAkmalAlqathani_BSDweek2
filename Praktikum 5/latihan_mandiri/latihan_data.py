from pymongo import MongoClient
from datetime import datetime, timedelta
import random

client = MongoClient('mongodb://localhost:27017')
db = client['latihan5']
collection = db['data_sensor']

sensor_ids = [f"S{str(i).zfill(2)}" for i in range(1, 11)]
categories = ["suhu", "tekanan", "kelembaban", "getaran"]
end_date = datetime.now()
start_date = end_date - timedelta(days=14)

docs = []
for i in range(5000):
    random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
    docs.append({
        "sensor_id": random.choice(sensor_ids),
        "nilai": round(random.uniform(20.0, 100.0), 2),
        "timestamp": start_date + timedelta(seconds=random_seconds),
        "category": random.choice(categories)
    })
    if len(docs) >= 500:
        collection.insert_many(docs)
        docs.clear()
if docs: collection.insert_many(docs) 