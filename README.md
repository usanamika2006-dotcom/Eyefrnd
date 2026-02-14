# Face Dirt Detection & Smart Compliment System 🎯

---

## Basic Details

### Team Name

[Your Team Name]

### Team Members

* Member 1: [Your Name] – [Your College]

### Hosted Project Link

[http://localhost:5000](http://localhost:5000)
(or add deployed link here)

---

## Project Description

A real-time face monitoring web application that detects visible dirt patches on the face using computer vision techniques — without AI models.
If no dirt is found, the system responds with a positive compliment.
The application also supports voice commands to stop detection.

---

## The Problem Statement

People often don’t notice visible dirt or stains on their face in real-time.
At the same time, constant negative feedback can affect user confidence.

We needed a system that:

* Detects significant dirt only (not eyebrows, contour, pimples, or birthmarks)
* Avoids over-detection
* Responds positively when the face is clean

---

## The Solution

We built a Flask-based web application using OpenCV that:

* Detects face using Haar Cascade
* Extracts skin region dynamically
* Calculates average skin tone
* Detects abnormal large patches only
* Ignores small spots like pimples and birthmarks
* Gives location-based feedback (forehead, cheek, chin)
* Gives compliments if clean
* Stops detection when user says "okey"
* Responds with "okey friend"

No AI models were used. Pure computer vision + adaptive color analysis.

---

# Technical Details

## Technologies/Components Used

### For Software:

* Languages used: Python
* Frameworks used: Flask
* Libraries used:

  * OpenCV (cv2)
  * NumPy
  * SpeechRecognition (for voice commands)
* Tools used:

  * VS Code
  * Git
  * Webcam

---

## Features

* Real-time face detection
* Adaptive skin tone detection (works for different skin colors)
* Dirt detection without hardcoded face zones
* Ignores:

  * Eyebrows
  * Eyes
  * Lips
  * Pimples
  * Birthmarks
* Location-based dirt feedback
* Auto compliment if face is clean
* Voice command support:

  * Say "okey" → system stops
  * App replies: "okey friend"
* No AI models used
* Lightweight and fast

---

# Implementation

## For Software

### Installation

```bash
git clone https://github.com/your-repo-name.git
cd your-repo-name
pip install -r requirements.txt
```

### Run

```bash
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---

# Project Documentation

## Screenshots

![Screenshot1](docs/screenshot1.png)
*Live camera feed with face detection*

![Screenshot2](docs/screenshot2.png)
*Dirt detected on forehead*

![Screenshot3](docs/screenshot3.png)
*Compliment displayed when face is clean*

---

## System Architecture

```
User Camera
    ↓
Flask Backend
    ↓
OpenCV Face Detection
    ↓
Skin Extraction (HSV)
    ↓
Average Skin Tone Calculation
    ↓
Anomaly Detection
    ↓
Response:
    - Dirt Location
    - Compliment
    - Voice Stop
```

---

## Application Workflow

1. User opens web app
2. Webcam captures frame
3. Face is detected
4. Skin area isolated
5. Average skin tone calculated
6. Large abnormal patch detection
7. If found → location message
8. If not → compliment
9. If user says "okey" → detection stops

---

# API Documentation

### Base URL:

```
http://localhost:5000
```

### GET /

* Loads main camera interface

---

### POST /detect

* Processes frame
* Returns detection result

Response Example:

```json
{
  "status": "success",
  "message": "There is something on your cheek"
}
```

or

```json
{
  "status": "success",
  "message": "You have a beautiful smile!"
}
```

---

# Demo

### Video

[Add YouTube / Drive Link Here]

Video demonstrates:

* Live detection
* Dirt detection accuracy
* Clean face compliment
* Voice command stopping system

---

# AI Tools Used (Transparency)

Tool Used: ChatGPT

Purpose:

* Code structuring
* Debugging assistance
* Architecture explanation
* README formatting

Percentage of AI-generated code: ~40–60%

Human Contributions:

* Core logic implementation
* Adaptive detection design
* Threshold tuning
* Flask integration
* Voice control logic
* Testing & optimization

---

# Team Contributions

* [Your Name]:

  * OpenCV detection logic
  * Flask backend
  * Voice command integration
  * Performance tuning
  * Frontend UI
  * Testing
  * Documentation
  * Deployment

---

# License

This project is licensed under the MIT License.

---

Made with ❤️ at TinkerHub

--- 
"# Eyefrnd" 
"# Eyefrnd" 
"# Eyefrnd" 
