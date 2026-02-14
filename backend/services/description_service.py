import cv2
import numpy as np
import os

cascade_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "haarcascade_frontalface_default.xml"))
face_cascade = cv2.CascadeClassifier(cascade_path)

def describe_person(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        return "No person detected"

    description = ["I see a person."]

    h, w, _ = image.shape
    center_pixel = image[h//2, w//2]

    if center_pixel[0] > 100:
        description.append("Likely male.")
    else:
        description.append("Likely female.")

    edges = cv2.Canny(gray, 50, 150)
    if np.mean(edges) > 25:
        description.append("Possibly wearing glasses.")

    top_region = image[0:int(h*0.25), :]
    avg_color = np.mean(top_region, axis=(0,1))

    if avg_color[2] > 150:
        description.append("Light colored hair.")
    else:
        description.append("Dark colored hair.")

    return " ".join(description)
