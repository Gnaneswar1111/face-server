from flask import Flask, request, jsonify
import face_recognition
import os

app = Flask(__name__)

# Load known faces
known_face_encodings = []
known_face_names = []

for filename in os.listdir("known_faces"):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image = face_recognition.load_image_file(f"known_faces/{filename}")
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_face_encodings.append(encoding[0])
            known_face_names.append(filename.split(".")[0])

@app.route("/recognize", methods=["POST"])
def recognize():
    file = request.files.get("image")
    if not file:
        return jsonify({"status": "error", "message": "No image uploaded"})

    image = face_recognition.load_image_file(file)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        return jsonify({"status": "no_face"})

    face_encoding = encodings[0]
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

    if True in matches:
        idx = matches.index(True)
        return jsonify({"status": "known", "name": known_face_names[idx]})
    else:
        return jsonify({"status": "unknown"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)