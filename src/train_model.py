import cv2
import os
import numpy as np
from PIL import Image

def train_model():
    path = os.path.join(os.path.dirname(__file__), '..', 'data')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(os.path.join(cv2.data.haarcascades, 'haarcascade_frontalface_default.xml'))

    def getImagesAndLabels(path):
        faceSamples = []
        ids = []
        
        # Iterate through all user directories
        for user_dir in os.listdir(path):
            user_path = os.path.join(path, user_dir)
            if not os.path.isdir(user_path):
                continue
                
            user_id = int(user_dir)
            
            for image_name in os.listdir(user_path):
                image_path = os.path.join(user_path, image_name)
                PIL_img = Image.open(image_path).convert('L') # convert it to grayscale
                img_numpy = np.array(PIL_img, 'uint8')
                
                faces = detector.detectMultiScale(img_numpy)
                for (x, y, w, h) in faces:
                    faceSamples.append(img_numpy[y:y+h, x:x+w])
                    ids.append(user_id)
        
        return faceSamples, ids

    print("Training faces. It will take a few seconds. Wait...")
    faces, ids = getImagesAndLabels(path)
    
    if not faces:
        print("No training data found.")
        return

    recognizer.train(faces, np.array(ids))

    # Save the model into models/trainer.yml
    trainer_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'trainer.yml')
    recognizer.write(trainer_path)
    print(f"{len(np.unique(ids))} users trained. Model saved at {trainer_path}")

if __name__ == "__main__":
    train_model()
