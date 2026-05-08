import json, time, random
import paho.mqtt.client as mqtt
from datetime import datetime

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "pabrik/sensor/suhu"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(BROKER, PORT, 60)
print(f"Terhubung ke {BROKER}")

for i in range(10):
    data = {
        "mesin": f"CNC-{random.randint(1,5):02d}",
        "suhu": round(random.uniform(60, 100), 2),
        "getaran": round(random.uniform(0.1, 0.5), 2),
        "timestamp": datetime.now().isoformat()
    }
    payload = json.dumps(data)
    client.publish(TOPIC, payload)
    print(f"[PUB] {payload}")
    time.sleep(2)
