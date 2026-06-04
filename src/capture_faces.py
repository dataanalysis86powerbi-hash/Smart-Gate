import cv2
import os
import sys
from db_manager import DBManager

def capture_faces():
    db = DBManager()
    name = input("Enter user name: ")
    user_id = db.add_user(name)
    
    # Create directory for user
    user_dir = os.path.join(os.path.dirname(__file__), '..', 'data', str(user_id))
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)

    # Load Haar Cascade
    cascade_path = os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml')
    face_cascade = cv2.CascadeClassifier(cascade_path)

    cam = cv2.VideoCapture(0)
    count = 0

    print(f"Starting capture for {name} (ID: {user_id}). Look at the camera...")

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            count += 1
            # Save the captured image into the user folder
            file_name = os.path.join(user_dir, f"{count}.jpg")
            cv2.imwrite(file_name, gray[y:y+h, x:x+w])
            
            # Display the video frame
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, f"Captured: {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        cv2.imshow('Capturing Faces', img)

        # Break if 'q' is pressed or count reaches 50
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 50:
            break

    print(f"Captured {count} samples for {name}")
    cam.release()
    cv2.destroyAllWindows()
    db.close()

if __name__ == "__main__":
    capture_faces()
