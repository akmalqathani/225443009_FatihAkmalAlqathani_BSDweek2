import matplotlib
matplotlib.use('TkAgg')
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client.praktikum6
collection = db.sensor

# Ambil data dan konversi ke DataFrame
cursor = collection.find({}, {"_id": 0})
df = pd.DataFrame(list(cursor))
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.set_index('timestamp', inplace=True)
df.sort_index(inplace=True)

# Visualisasi Suhu
plt.figure(figsize=(12, 6))
for mesin in df['mesin'].unique():
    data_mesin = df[df['mesin'] == mesin]
    plt.plot(data_mesin.index, data_mesin['suhu'], marker='o', label=f'Mesin {mesin}')
plt.title('Suhu Mesin dari Waktu ke Waktu')
plt.legend()
plt.savefig('suhu_plot.png')
plt.show()
