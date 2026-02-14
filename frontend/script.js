const video = document.getElementById('video');
const statusDiv = document.createElement('div');
statusDiv.style.position = 'absolute';
statusDiv.style.top = '10px';
statusDiv.style.left = '10px';
statusDiv.style.color = 'white';
statusDiv.style.backgroundColor = 'rgba(0,0,0,0.5)';
statusDiv.style.padding = '5px';
document.body.appendChild(statusDiv);

function updateStatus(text) {
    statusDiv.innerText = text;
}

// Access Camera
navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        updateStatus("Camera Active. Say 'Face', 'Description', or 'Bye'");
    })
    .catch(err => {
        console.error(err);
        updateStatus("Camera Error: " + err.message);
    });

// Speech Synthesis
function speak(text) {
    window.speechSynthesis.cancel(); // Stop previous
    const speech = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(speech);
}

// Backend Capture
function capture(endpoint) {
    updateStatus("Processing...");
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);

    canvas.toBlob(blob => {
        const formData = new FormData();
        formData.append("image", blob);

        // Use absolute URL to allow running frontend on a different port (e.g. Live Server)
        fetch("http://127.0.0.1:5000/" + endpoint, {
            method: "POST",
            body: formData
        })
            .then(res => res.json())
            .then(data => {
                updateStatus("Result: " + data.message);
                speak(data.message);
            })
            .catch(err => {
                console.error(err);
                updateStatus("Error: " + err.message);
                speak("Error connecting to server.");
            });
    });
}

// Shake Detection
let lastX = 0, lastY = 0, lastZ = 0;
let lastTime = 0;
const shakeThreshold = 15;
let shakeCount = 0;
let lastShakeTime = 0;

window.addEventListener('devicemotion', (event) => {
    const current = event.accelerationIncludingGravity;
    if (!current) return;

    const time = new Date().getTime();
    if ((time - lastTime) > 100) {
        const diffTime = (time - lastTime);
        lastTime = time;

        const speed = Math.abs(current.x + current.y + current.z - lastX - lastY - lastZ) / diffTime * 10000;

        if (speed > shakeThreshold) {
            const now = new Date().getTime();
            if (now - lastShakeTime > 1000) { // Debounce 1s
                shakeCount++;
                lastShakeTime = now;

                if (shakeCount >= 2) {
                    capture('scan'); // Double shake -> Face Clean
                    speak("Double shake detected. Scanning face.");
                    shakeCount = 0;
                }
            }
        }

        lastX = current.x;
        lastY = current.y;
        lastZ = current.z;
    }
});

// Voice Command (Web Speech API)
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

if (SpeechRecognition) {
    const recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        console.log("Voice recognition started");
    };

    recognition.onresult = (event) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript.toLowerCase().trim();
        console.log("Heard:", transcript);
        updateStatus("Heard: " + transcript);

        if (transcript.includes("face")) {
            speak("Face mode activated.");
            capture('scan');
        } else if (transcript.includes("description") || transcript.includes("describe")) {
            speak("Description mode activated.");
            capture('describe');
        } else if (transcript.includes("bye")) {
            speak("Goodbye Friend.");
            // Optional: Close app or stop stream?
        }
    };

    recognition.onerror = (event) => {
        console.error("Speech error", event);
        if (event.error === 'not-allowed') {
            updateStatus("Mic access denied.");
        }
    };

    recognition.start();
} else {
    updateStatus("Voice Recognition not supported in this browser.");
}
