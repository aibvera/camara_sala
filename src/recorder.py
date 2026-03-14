import os
import subprocess
import signal

class StreamRecorder:
    def __init__(self, rtsp_url, output_file):
        self.rtsp_url = rtsp_url
        self.output_file = output_file
        self.temp_file = output_file.replace(".mp4", ".ts")
        self.process = None

    def start(self):
        cmd = [
            "ffmpeg",
            "-y",
            "-rtsp_transport", "tcp",
            "-i", self.rtsp_url,
            "-c", "copy",
            "-f", "mpegts",
            self.temp_file
        ]

        self.process = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def stop(self):
        if not self.process:
            print("[WARN] stop() llamado pero ffmpeg nunca inicio")
            return

        # Enviar SIGINT para que ffmpeg cierre bien el archivo
        try:
            self.process.send_signal(signal.SIGINT)
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            print("[WARN] ffmpeg no respondio a SIGINT, matando proceso")
            self.process.kill()

        # Convertir solo si el archivo .ts existe y tiene tamaño > 0
        if os.path.exists(self.temp_file) and os.path.getsize(self.temp_file) > 0:
            subprocess.run([
                "ffmpeg", "-y",
                "-i", self.temp_file,
                "-c", "copy",
                self.output_file
            ])
        else:
            print(f"[WARN] Archivo {self.temp_file} no existe o esta vacio. No se genera MP4.")

        # Eliminar archivo temporal
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
