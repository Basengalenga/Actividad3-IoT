import paho.mqtt.client as mqtt
import psycopg2
import json

# 1. Configuración de conexiones
DB_PARAMS = {
    "host": "localhost", # O la IP de tu contenedor/servidor
    "database": "epicmomo",
    "user": "admin",
    "password": "admin"
}

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
# Usamos el comodín # para recibir TODO lo que esté bajo sensores/datos/
MQTT_TOPIC = "sensores/datos/#"

# 2. Función para insertar en PostgreSQL
def save_to_db(table, topic, payload, value):
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        cur = conn.cursor()
        
        # Query dinámico según la tabla (int o float)
        query = f"""
            INSERT INTO {table} (topic, payload, value) 
            VALUES (%s, %s, %s)
        """
        cur.execute(query, (topic, payload, value))
        
        conn.commit()
        cur.close()
        conn.close()
        print(f" Guardado en {table}: {value}")
    except Exception as e:
        print(f" Error de DB: {e}")

# 3. Callback: Qué hacer cuando llega un mensaje
def on_message(client, userdata, msg):
    try:
        # Decodificar el mensaje
        topic = msg.topic
        payload_str = msg.payload.decode()
        data = json.loads(payload_str)
        valor = data.get("valor")

        print(f"Mensaje recibido en {topic}: {valor}")

        # Lógica de ruteo según el tópico (Requisito UPY)
        if "enteros" in topic:
            save_to_db("lake_raw_data_int", topic, payload_str, int(valor))
        elif "flotantes" in topic:
            save_to_db("lake_raw_data_float", topic, payload_str, float(valor))

    except Exception as e:
        print(f" Error al procesar mensaje: {e}")

# 4. Configuración del Cliente MQTT
client = mqtt.Client()
client.on_message = on_message

try:
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.subscribe(MQTT_TOPIC) # Se suscribe a los tópicos [cite: 18]
    print(f"Capturador listo. Escuchando {MQTT_TOPIC}...")
    
    # Mantiene el script vivo escuchando mensajes permanentemente
    client.loop_forever()

except KeyboardInterrupt:
    print("\nCapturador detenido.")