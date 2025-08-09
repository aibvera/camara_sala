from ultralytics import YOLO

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
