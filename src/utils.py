import cv2
import numpy as np

def frame_changed(prev_frame, curr_frame, threshold_percent=10, diff_threshold=30):
    """
    Detecta si curr_frame cambió más de threshold_percent% respecto a prev_frame.

    threshold_percent: porcentaje de píxeles diferentes para considerar que hubo cambio.
    diff_threshold: diferencia mínima de intensidad para considerar un píxel como cambiado.
    """
    if prev_frame is None:
        return False, 0.

    # Convertir a escala de grises
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

    # Diferencia absoluta
    diff = cv2.absdiff(prev_gray, curr_gray)

    # Umbralizar para contar solo cambios significativos
    _, diff_bin = cv2.threshold(diff, diff_threshold, 255, cv2.THRESH_BINARY)

    # Calcular porcentaje de píxeles cambiados
    changed_pixels = np.count_nonzero(diff_bin)
    total_pixels = diff_bin.size
    percent_changed = (changed_pixels / total_pixels) * 100

    return percent_changed > threshold_percent, percent_changed
