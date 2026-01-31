import psycopg2
import time

def init_db():
    # Datos de conexión directos (como pediste para el proyecto escolar)
    conn_params = {
        "host": "db", # Nombre del servicio en docker-compose
        "database": "epicmomo",
        "user": "admin",
        "password": "admin"
    }

    commands = [
        """
        CREATE TABLE IF NOT EXISTS lake_raw_data_int (
            id BIGSERIAL PRIMARY KEY,
            topic TEXT NOT NULL,
            payload TEXT NOT NULL,
            value BIGINT NOT NULL,
            ts TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS lake_raw_data_float (
            id BIGSERIAL PRIMARY KEY,
            topic TEXT NOT NULL,
            payload TEXT NOT NULL,
            value DOUBLE PRECISION NOT NULL,
            ts TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    ]

    print("Esperando a que Postgres despierte...")
    while True:
        try:
            conn = psycopg2.connect(**conn_params)
            cur = conn.cursor()
            for command in commands:
                cur.execute(command)
            conn.commit()
            cur.close()
            conn.close()
            print("Tablas creadas exitosamente.")
            break
        except Exception as e:
            print(f"Error conectando (reintentando en 2s): {e}")
            time.sleep(2)

if __name__ == "__main__":
    init_db()