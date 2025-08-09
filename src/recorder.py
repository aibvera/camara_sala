import os
import subprocess

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
            "-i", self.rtsp_url,
            "-c", "copy",
            "-f", "mpegts",
            self.temp_file
        ]
        self.process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
            
            # Convertir a mp4
            subprocess.run([
                "ffmpeg", "-y",
                "-i", self.temp_file,
                "-c", "copy",
                self.output_file
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Eliminar el archivo .ts temporal
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
