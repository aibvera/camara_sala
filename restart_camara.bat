@echo off
echo ============================================
echo   Reinicio robusto de contenedor camara-sala
echo ============================================

REM --- 0. Variables ---
SET CONTAINER_NAME=camara-sala
SET IMAGE_NAME=camara-image
SET VIDEO_PATH=C:\Users\aleja\Videos\videos_camara
SET ENV_FILE=.env

REM --- 1. Verificar .env ---
IF NOT EXIST "%ENV_FILE%" (
    echo ERROR: No se encontro el archivo .env en esta carpeta.
    pause
    exit /b 1
)

REM --- 2. Detener contenedor si existe ---
echo Verificando contenedor existente...
docker ps -a --format "{{.Names}}" | findstr /I "%CONTAINER_NAME%" >nul
IF %ERRORLEVEL%==0 (
    echo Contenedor encontrado. Deteniendo...
    docker stop %CONTAINER_NAME%
    echo Eliminando contenedor...
    docker rm %CONTAINER_NAME%
) ELSE (
    echo No existe contenedor previo.
)

REM --- 3. Eliminar imagen si existe ---
echo Verificando imagen existente...
docker images --format "{{.Repository}}" | findstr /I "%IMAGE_NAME%" >nul
IF %ERRORLEVEL%==0 (
    echo Imagen encontrada. Eliminando...
    docker rmi %IMAGE_NAME% -f
) ELSE (
    echo No existe imagen previa.
)

REM --- 4. Construir nueva imagen ---
echo Construyendo nueva imagen %IMAGE_NAME%...
docker build -t %IMAGE_NAME% .

IF %ERRORLEVEL% NEQ 0 (
    echo ERROR: Fallo al construir la imagen.
    pause
    exit /b 1
)

REM --- 5. Crear carpeta de videos si no existe ---
IF NOT EXIST "%VIDEO_PATH%" (
    echo Creando carpeta de videos en %VIDEO_PATH%...
    mkdir "%VIDEO_PATH%"
)

REM --- 6. Levantar contenedor ---
echo Levantando contenedor %CONTAINER_NAME%...

docker run -d ^
  --name %CONTAINER_NAME% ^
  --restart unless-stopped ^
  --env-file "%ENV_FILE%" ^
  -v "%VIDEO_PATH%:/app/output" ^
  %IMAGE_NAME%

IF %ERRORLEVEL%==0 (
    echo ============================================
    echo   Contenedor %CONTAINER_NAME% levantado con exito
    echo   Videos en: %VIDEO_PATH%
    echo ============================================
) ELSE (
    echo ERROR: No se pudo iniciar el contenedor.
)

pause