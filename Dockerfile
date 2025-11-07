FROM python:3.12-slim

# Evita que Python genere archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala ffmpeg y dependencias mínimas del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea directorio de trabajo dentro del contenedor
WORKDIR /app

# venv y proyecto al directorio
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Comando por defecto al ejecutar el contenedor
CMD ["python", "main.py"]
