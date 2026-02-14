import requests
import cv2
import numpy as np

# Create a dummy image (gray face-like shape)
img = np.zeros((300, 300, 3), dtype=np.uint8)
cv2.rectangle(img, (100, 100), (200, 200), (255, 255, 255), -1) # White square as face
cv2.imwrite('test_face.jpg', img)

base_url = 'http://127.0.0.1:5000'

try:
    # Test Root
    resp = requests.get(base_url + '/')
    print(f"Root: {resp.status_code}")

    # Test Scan
    files = {'image': open('test_face.jpg', 'rb')}
    resp = requests.post(base_url + '/scan', files=files)
    print(f"Scan: {resp.json()}")

    # Test Describe
    files = {'image': open('test_face.jpg', 'rb')}
    resp = requests.post(base_url + '/describe', files=files)
    print(f"Describe: {resp.json()}")

    # Test Voice Command
    resp = requests.post(base_url + '/voice-command', json={'command': 'face'})
    print(f"Voice: {resp.json()}")

except Exception as e:
    print(f"Test failed: {e}")
