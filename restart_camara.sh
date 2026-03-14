#!/bin/bash

echo "============================================"
echo "  Reinicio robusto de contenedor camara-sala"
echo "============================================"

# --- 0. Variables ---
CONTAINER_NAME="camara-sala"
IMAGE_NAME="camara-image"
VIDEO_PATH="/home/aleja/videos_camara"   # Ajusta si quieres otra ruta
ENV_FILE=".env"

# --- 1. Verificar .env ---
if [ ! -f "$ENV_FILE" ]; then
    echo "ERROR: No se encontró el archivo .env en esta carpeta."
    exit 1
fi

# --- 2. Detener contenedor si existe ---
echo "Verificando contenedor existente..."
if docker ps -a --format "{{.Names}}" | grep -qi "^${CONTAINER_NAME}$"; then
    echo "Contenedor encontrado. Deteniendo..."
    docker stop "$CONTAINER_NAME"
    echo "Eliminando contenedor..."
    docker rm "$CONTAINER_NAME"
else
    echo "No existe contenedor previo."
fi

# --- 3. Eliminar imagen si existe ---
echo "Verificando imagen existente..."
if docker images --format "{{.Repository}}" | grep -qi "^${IMAGE_NAME}$"; then
    echo "Imagen encontrada. Eliminando..."
    docker rmi -f "$IMAGE_NAME"
else
    echo "No existe imagen previa."
fi

# --- 4. Construir nueva imagen ---
echo "Construyendo nueva imagen $IMAGE_NAME..."
docker build -t "$IMAGE_NAME" .

if [ $? -ne 0 ]; then
    echo "ERROR: Fallo al construir la imagen."
    exit 1
fi

# --- 5. Crear carpeta de videos si no existe ---
if [ ! -d "$VIDEO_PATH" ]; then
    echo "Creando carpeta de videos en $VIDEO_PATH..."
    mkdir -p "$VIDEO_PATH"
fi

# --- 6. Levantar contenedor ---
echo "Levantando contenedor $CONTAINER_NAME..."

docker run -d \
  --name "$CONTAINER_NAME" \
  --restart unless-stopped \
  --env-file "$ENV_FILE" \
  -v "$VIDEO_PATH:/app/output" \
  "$IMAGE_NAME"

if [ $? -eq 0 ]; then
    echo "============================================"
    echo "  Contenedor $CONTAINER_NAME levantado con éxito"
    echo "  Videos en: $VIDEO_PATH"
    echo "============================================"
else
    echo "ERROR: No se pudo iniciar el contenedor."
fi