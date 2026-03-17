import psutil
import os
import time
from datetime import datetime, timedelta, timezone   # ← agregado
from src.config import HOST_URL, RTSP_URL, MODEL_PATH, OUTPUT_PATH, GRACE_PERIOD, CONF_TH, SINGLE_CORE
from src.camera import CameraStream
from src.detector import PersonDetector
from src.recorder import StreamRecorder
from src.ping import successful_ping
from src.utils import frame_changed

# Configuración de zona horaria de Lima (UTC-5)
LIMA_TZ = timezone(timedelta(hours=-5))

def main():

    # Prueba de conexión al host
    if successful_ping(HOST_URL):
        print('[INFO] Ping a cámara exitoso')
    else:
        print('[ERROR] No se pudo hacer ping a cámara')
        return

    # Objetos
    camera = CameraStream(RTSP_URL)
    detector = PersonDetector(MODEL_PATH, CONF_TH)

    # Probar conexión antes del bucle
    if not camera.is_connected():
        return

    # Probar disponibilidad de predictor
    if not detector.is_ready():
        return

    # Variables generales
    recorder = None
    last_seen = 0
    recording = False
    prev_frame = None

    # Bucle central
    try:
        print('[INFO] Bucle iniciado')
        while True:

            # Capturar cuadro del stream de la cámara
            frame = camera.get_frame()
            if frame is None:
                print('[ERROR] No se pudo capturar un cuadro del stream')
                break

            # Evaluar si ha habido movimiento en la transmisión
            changed, _ = frame_changed(prev_frame, frame, threshold_percent=5)
            prev_frame = frame
            if not changed:
                continue

            # Detectar si hay una persona
            detected = detector.detect(frame)
            if detected:
                last_seen = time.time()

                # Empezar a grabar
                if not recording:
                    print("[INFO] Persona detectada → Iniciando grabación")

                    # Crear carpeta con fecha dentro de OUTPUT_PATH
                    os.makedirs(OUTPUT_PATH, exist_ok=True)
                    date_folder = datetime.now(LIMA_TZ).strftime("%Y-%m-%d")
                    save_dir = os.path.join(OUTPUT_PATH, date_folder)
                    os.makedirs(save_dir, exist_ok=True)

                    # Nombre del archivo
                    timestamp = datetime.now(LIMA_TZ).strftime("%H%M%S")
                    output_file = os.path.join(save_dir, f"detec_{timestamp}.mp4")

                    # Iniciar grabación
                    recorder = StreamRecorder(RTSP_URL, output_file)
                    recorder.start()
                    recording = True

            # Dejar de grabar si no hay detección por cierto tiempo
            if recording and (time.time() - last_seen > GRACE_PERIOD):
                print("[INFO] No hay persona → Deteniendo grabación")
                recorder.stop()
                recorder = None
                recording = False
                print("[INFO] Grabación detenida y guardada")

    except KeyboardInterrupt:
        pass
    finally:
        if recorder and recording:
            recorder.stop()
        camera.release()


if __name__ == '__main__':
    
    # Forzar uso del núcleo 0 en Windows y Linux (opcional)
    if SINGLE_CORE:
        try:
            p = psutil.Process(os.getpid())
            p.cpu_affinity([0])
            print("[INFO] Afinidad de CPU fijada a un solo núcleo")
        except Exception as e:
            print(f"[WARN] No se pudo fijar afinidad de CPU: {e}")

    # Programa
    main()
