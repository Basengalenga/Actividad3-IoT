# Actividad3-IoT
Diagrama para la actividad
generator.py > brocker > suscriber.py > postgres > streamlit

EL docker-compose crea una base de datos un brocker, y utiliza un script de python para crear las tablas del postgres. Al igual que hostea el streamlit
### El generator y el suscriber, funcionan fuera del docker

# env
Antes de todo, hagan su ambiente virtual e instalen las libreríás
Primero se hace el docker compose up y luego se corre en dos terminales distintas el generator y el suscriber


