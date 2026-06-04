import cv2
import os
import time
from datetime import datetime
from db_manager import DBManager

def recognize_faces():
    db = DBManager()
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    trainer_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trainer.yml')
    
    if not os.path.exists(trainer_path):
        print("Model not found. Please train the model first.")
        return

    recognizer.read(trainer_path)
    cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Load users for mapping ID to Name
    users_raw = db.get_users()
    users = {u[0]: u[1] for u in users_raw}

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Cooldown settings
    last_log_time = {} # {user_id: timestamp}
    COOLDOWN_SECONDS = 10
    UNKNOWN_COOLDOWN = 5
    last_unknown_log = 0

    print("Starting Recognition. Press 'q' to exit.")

    while True:
        ret, img = cam.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            # LBPH: Lower confidence means better match. Threshold ~100.
            if confidence < 75:
                name = users.get(id, "Unknown")
                status = "AUTHORIZED"
                color = (0, 255, 0)
                
                # Cooldown check
                current_time = time.time()
                if id not in last_log_time or (current_time - last_log_time[id]) > COOLDOWN_SECONDS:
                    db.log_access(id, status, round(100 - confidence, 2))
                    last_log_time[id] = current_time
                    print(f"Access Granted: {name} ({round(100-confidence, 2)}%)")
            else:
                id = None
                name = "Intruder"
                status = "DENIED"
                color = (0, 0, 255)
                
                current_time = time.time()
                if (current_time - last_unknown_log) > UNKNOWN_COOLDOWN:
                    # Intruder Protocol: Capture image
                    intruder_dir = os.path.join(os.path.dirname(__file__), '..', 'data', 'intruders')
                    if not os.path.exists(intruder_dir):
                        os.makedirs(intruder_dir)
                    
                    img_name = f"intruder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                    img_path = os.path.join(intruder_dir, img_name)
                    cv2.imwrite(img_path, img)
                    
                    db.log_access(None, status, round(confidence, 2), img_path)
                    last_unknown_log = current_time
                    print(f"Access Denied! Photo captured: {img_name}")

            cv2.putText(img, str(name), (x+5, y-5), font, 1, color, 2)
            cv2.putText(img, f"{round(100 - confidence, 2)}%", (x+5, y+h-5), font, 1, (255, 255, 0), 1)
            cv2.rectangle(img, (x, y), (x+w, y+h), color, 2)

        cv2.imshow('Smart-Gate Access Control', img)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()
    db.close()

if __name__ == "__main__":
    recognize_faces()
