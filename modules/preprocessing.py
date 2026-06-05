
import cv2
import numpy as np

def preprocess_image(image):

    image_array = np.array(image.convert("RGB"))

    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY
    )

    denoised = cv2.fastNlMeansDenoising(gray)

    threshold = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    return threshold
