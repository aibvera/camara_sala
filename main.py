import os
import time
from src.config import RTSP_URL, MODEL_PATH, OUTPUT_PATH, GRACE_PERIOD, CONF_TH
from src.camera import CameraStream
from src.detector import PersonDetector
from src.recorder import StreamRecorder

camera = CameraStream(RTSP_URL)
detector = PersonDetector(MODEL_PATH, CONF_TH)

recorder = None
last_seen = 0
recording = False

try:
    print('Iniciando bucle')
    while True:

        # Capturar cuadro del stream de la cámara
        frame = camera.get_frame()
        if frame is None:
            break

        # Detectar si hay una persona
        detected = detector.detect(frame)

        if detected:
            last_seen = time.time()
            if not recording:
                print("[INFO] Persona detectada → Iniciando grabación")

                # Crear carpeta con fecha dentro de OUTPUT_PATH
                os.makedirs(OUTPUT_PATH, exist_ok=True)
                date_folder = time.strftime("%Y-%m-%d")
                save_dir = os.path.join(OUTPUT_PATH, date_folder)
                os.makedirs(save_dir, exist_ok=True)

                # Nombre del archivo
                timestamp = time.strftime("%H%M%S")  # Solo hora, min, seg
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

except KeyboardInterrupt:
    pass
finally:
    if recorder and recording:
        recorder.stop()
    camera.release()
