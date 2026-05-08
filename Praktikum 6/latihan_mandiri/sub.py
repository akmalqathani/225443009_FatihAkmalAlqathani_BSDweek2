import paho.mqtt.client as mqtt
from pymongo import MongoClient
import json
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()
client_mongo = MongoClient(os.getenv("MONGO_URI"))
db = client_mongo["latihan6"]
collection = db["produksi_mqtt"] 

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "pabrik/produksi"
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Terhubung ke MQTT Broker sebagai SUBSCRIBER")
        client.subscribe(TOPIC)
        print(f"Menunggu data dari topik: {TOPIC}...\n")
    else:
        print(f"Gagal terhubung dengan kode: {rc}")
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        payload['timestamp'] = datetime.now(timezone.utc)
        reject_rate = (payload['reject'] / payload['jumlah']) * 100
        payload['reject_rate'] = round(reject_rate, 2) 
        if reject_rate > 5.0:
            print(f"⚠️ PERINGATAN! Reject rate tinggi: {reject_rate:.2f}% pada {payload['mesin']} (Batch {payload['batch']})")
            payload['peringatan'] = True # Tambahkan field peringatan: true
        result = collection.insert_one(payload)
        print(f"[MONGO] Tersimpan: Batch {payload['batch']} | Reject: {reject_rate:.2f}%")
    except Exception as e:
        print(f"Error memproses data: {e}")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message


print("Mencoba terhubung ke broker...")
mqtt_client.connect(BROKER, PORT, 60)

try:
    mqtt_client.loop_forever()
except KeyboardInterrupt:
    print("\nMematikan subscriber...")
finally:
    client_mongo.close()

