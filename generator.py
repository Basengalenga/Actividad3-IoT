import paho.mqtt.client as mqtt
import time
import random
import json

# Configuración del Broker (puedes usar tu 'Factoria-remota' o localhost)
BROKER = "localhost" 
PORT = 1883
TOPIC_INT = "sensores/datos/enteros"
TOPIC_FLOAT = "sensores/datos/flotantes"

# Inicializar cliente
client = mqtt.Client()

try:
    client.connect(BROKER, PORT, 60)
    print(f"Conectado al broker {BROKER}. Enviando datos...")
    
    while True:
        # 1. Generar valores aleatorios (Requisito: Integer y Float) 
        val_int = random.randint(0, 100)
        val_float = round(random.uniform(10.0, 50.0), 2)
        
        # 2. Crear payloads (JSON facilita el trabajo del capturer), convierte el diccionario en un string json
        payload_int = json.dumps({"valor": val_int})
        payload_float = json.dumps({"valor": val_float})
        
        # 3. Publicar en tópicos diferentes 
        client.publish(TOPIC_INT, payload_int)
        client.publish(TOPIC_FLOAT, payload_float)
        
        print(f"Publicado: Int={val_int} en {TOPIC_INT} | Float={val_float} en {TOPIC_FLOAT}")
        
        # Esperar un poco para no saturar
        time.sleep(2)

except KeyboardInterrupt:
    print("\nGenerador detenido.")
finally:
    client.disconnect()