import subprocess
import platform

def successful_ping(host: str, count: int = 2, timeout: int = 2) -> bool:
    """
    Retorna True si el host responde al ping, False si no.
    Compatible con Linux, macOS y Windows.
    """
    # Cambia los parámetros según el sistema
    param = "-n" if platform.system().lower() == "windows" else "-c"
    timeout_param = "-w" if platform.system().lower() == "windows" else "-W"

    try:
        result = subprocess.run(
            ["ping", param, str(count), timeout_param, str(timeout), host],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error al ejecutar successful_ping: {e}")
        return False
