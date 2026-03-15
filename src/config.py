from decouple import Config, RepositoryEnv
from pathlib import Path

# Ruta al archivo .env en la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
env = Config(RepositoryEnv(BASE_DIR / ".env"))

# Variables de entorno
HOST_URL = env("HOST_URL")
RTSP_URL = env("RTSP_URL")
OUTPUT_PATH = env("OUTPUT_PATH", default="output")
MODEL_PATH = env("MODEL_PATH", default="yolov8n.pt")
GRACE_PERIOD = env("GRACE_PERIOD", cast=int, default=60)
CONF_TH = env("CONF_TH", cast=float, default=0.5)
SINGLE_CORE = env("SINGLE_CORE", cast=bool, default=False)
