import cv2
import numpy as np
import os
from services.compliment_service import generate_compliment

# Load Haar Cascade properly
cascade_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "haarcascade_frontalface_default.xml")
)
face_cascade = cv2.CascadeClassifier(cascade_path)


def detect_face_clean(image, ignored_regions):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=6,
        minSize=(120, 120)
    )

    if len(faces) == 0:
        return "No face detected"

    for (x, y, w, h) in faces:

        face_region = image[y:y+h, x:x+w]

        # --------------------------------
        # STEP 1: Convert to HSV
        # --------------------------------
        hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)

        # Skin color range (works for most skin tones)
        lower_skin = np.array([0, 30, 60], dtype=np.uint8)
        upper_skin = np.array([25, 170, 255], dtype=np.uint8)

        skin_mask = cv2.inRange(hsv, lower_skin, upper_skin)

        # --------------------------------
        # STEP 2: Clean noise (remove pimples/birthmarks)
        # --------------------------------
        kernel = np.ones((5, 5), np.uint8)

        # Remove small white noise
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel)

        # Close small gaps
        skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel)

        # --------------------------------
        # STEP 3: Extract only skin area
        # --------------------------------
        skin_only = cv2.bitwise_and(face_region, face_region, mask=skin_mask)

        # --------------------------------
        # STEP 4: Detect abnormal patches
        # --------------------------------
        avg_color = np.mean(skin_only[skin_mask > 0], axis=0)

        if avg_color is None or len(avg_color) == 0:
            return generate_compliment()

        diff = cv2.absdiff(skin_only, avg_color.astype(np.uint8))
        gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

        _, anomaly_mask = cv2.threshold(gray_diff, 45, 255, cv2.THRESH_BINARY)

        # Clean small spots again
        anomaly_mask = cv2.morphologyEx(anomaly_mask, cv2.MORPH_OPEN, kernel)

        contours, _ = cv2.findContours(
            anomaly_mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        significant_found = False

        for contour in contours:
            area = cv2.contourArea(contour)

            # Ignore small pimples / birthmarks
            if area > 5000:   # IMPORTANT threshold
                significant_found = True

                cx, cy, cw, ch = cv2.boundingRect(contour)
                relative_y = cy / h

                if relative_y < 0.33:
                    return "There is something on your forehead"
                elif relative_y < 0.66:
                    return "There is something on your cheek"
                else:
                    return "There is something near your chin"

        if not significant_found:
            return generate_compliment()

    return generate_compliment()
