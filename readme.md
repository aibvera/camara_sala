# Detección de personas y generación de video

Básicamente eso. El video lo traté de guardar con audio pero creo que el stream no devuelve audio.

## Antes de levantar
- El .env debe estar creado y lleno en el directorio raiz.

## Levantar la aplicación

- En Linux:
    1. Cambia la ruta de VIDEO_PATH (del `.sh`) a la que quieras.
    2. Dar permisos de ejecución: `chmod +x restart_camara.sh`
    3. Ejecutar: `./restart_camara.sh`

- En Windows:
    1. Cambia la ruta de VIDEO_PATH (del `.bat`) a la que quieras.
    2. Ejecutar: `./restart_camara.bat`

## Copiar carpeta de videos a otra pc

- Editar y ejecutar: `scp -r usuario@192.168.1.XXX:/home/ale/videos_camara C:\Users\aleja\Desktop\`

## Comando para limpiar completamente Docker

- `docker system prune -a --volumes`

---

**ABV 2025-2026**