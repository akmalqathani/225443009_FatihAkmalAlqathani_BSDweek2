import paho.mqtt.client as mqtt
import random
import time
import json

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "pabrik/produksi"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)
print(f"Terhubung ke {BROKER} sebagai PUBLISHER")

print("Memulai pengiriman data produksi...")

for i in range(15):
    data = {
        "batch": f"BTH-{random.randint(1000, 9999)}",
        "mesin": f"Mesin-{random.randint(1,3)}",
        "jumlah": random.randint(100, 500),
        "reject": random.randint(0, 50)
    }
    
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    
    print(f"[KIRIM {i+1}/15] {payload}")
    time.sleep(3) 

print("Pengiriman selesai, memutus koneksi...")
client.disconnect()

