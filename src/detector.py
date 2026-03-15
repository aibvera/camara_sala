from ultralytics import YOLO
import numpy as np

class PersonDetector:
    def __init__(self, model_name, conf_threshold):
        self.model = YOLO(model_name)
        self.conf_threshold = conf_threshold

    def detect(self, frame):
        # Ejecutar predicción y devolver True si detecta persona
        results = self.model.predict(
            frame,
            conf=self.conf_threshold,
            verbose=False,
            device="cpu",
            classes=[0]  # Solo detectar clase "persona"
        )

        # Si hay al menos 1 caja, devuelve True (hay una persona)
        return len(results[0].boxes) > 0
    
    def is_ready(self):
        """
        Verifica si el modelo puede predecir correctamente.
        Retorna True si el modelo funciona, False si falla.
        """
        try:
            # Crear un frame vacío (1x1 pixel)
            dummy = np.zeros((1, 1, 3), dtype=np.uint8)

            # Intentar una predicción mínima
            self.model.predict(
                dummy,
                conf=self.conf_threshold,
                verbose=False,
                device="cpu",
                classes=[0]
            )
            print(f"[INFO] Predicción de prueba exitosa")

            return True

        except Exception as e:
            print(f"[ERROR] El modelo no puede predecir: {e}")
            return False
