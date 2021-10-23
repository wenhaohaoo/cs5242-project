import os
import argparse
from pathlib import Path

import cv2
from tqdm import tqdm

def preprocess(dir):
    print(f'Search term: {dir}')

    image_list = os.listdir(f'images/{dir}')
    Path(f'images/{dir}/faces').mkdir(parents=True, exist_ok=True)

    # Load cascade
    face_cascade = cv2.CascadeClassifier('trained_models/haarcascade_frontalface_default.xml')

    count = 0
    for image in tqdm(image_list, desc=f'search_term={dir}'):
        if image != 'faces':
            try:
                # Read the input image
                img = cv2.imread(f'images/{dir}/{image}')

                # Convert into grayscale
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # Detect faces
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)

                for (x, y, w, h) in faces:

                    # Crop the detected faces
                    crop = gray[y:y+h, x:x+w]

                    # Resize the face
                    resized = cv2.resize(crop, (128, 128), interpolation=3)

                    # Save the processed image
                    cv2.imwrite(f'images/{dir}/faces/{count}.jpg', resized)

                    count += 1
            except Exception as e:
                print(f'failed {count}, {image}, {e}')
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        default='happy man',
        help='directory of images to preprocess',
    )

    args = parser.parse_args()
    preprocess(args.s)
