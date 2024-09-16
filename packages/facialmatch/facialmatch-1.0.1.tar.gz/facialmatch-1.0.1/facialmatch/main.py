import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load pre-trained Haar Cascade model for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def preprocess_face(face_image):
    """ Preprocess face by resizing and normalizing pixel values. """
    face_image = cv2.resize(face_image, (160, 160))  # Resizing to a fixed size
    face_image = face_image.astype('float32') / 255.0  # Normalize pixel values
    return face_image

def get_face_embedding(face_image):
    """ Generate a simple face embedding using basic convolutions and pooling. """
    face_image = preprocess_face(face_image)
    
    # Using simple convolution and pooling to create an embedding
    face_image = np.expand_dims(face_image, axis=0)  # Add batch dimension
    conv = cv2.filter2D(face_image[0], -1, np.ones((3, 3), np.float32))  # Simple convolution
    pooled = cv2.resize(conv, (40, 40))  # Simple pooling (downsample)
    
    embedding = pooled.flatten()  # Flatten the matrix into a 1D embedding
    return embedding

def get_face_from_image(image_path):
    """ Detect faces and return the first detected face from an image file path. """
    # Check if the file exists
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file '{image_path}' not found.")

    # Attempt to read the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read the image from '{image_path}'. Please check if the file is corrupted or in an unsupported format.")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect face using Haar Cascade
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    if len(faces) == 0:
        raise ValueError(f"No face detected in the image '{image_path}'.")

    (x, y, w, h) = faces[0]
    face_image = image[y:y+h, x:x+w]
    return face_image

def compare_faces(image_path1, image_path2, minimum_similarity=0.75):
    """ Compare faces in two images using file paths and return similarity. """
    try:
        # Extract faces from the images
        face1 = get_face_from_image(image_path1)
        face2 = get_face_from_image(image_path2)

        # Generate embeddings
        embedding1 = get_face_embedding(face1)
        embedding2 = get_face_embedding(face2)

        # Calculate similarity using cosine similarity
        similarity = cosine_similarity([embedding1], [embedding2])[0][0]
        similarity_percentage = round(float(similarity * 100), 2)
        match = bool(similarity > minimum_similarity)

        result = {
            "similarity": similarity_percentage,
            "match": match
        }
        return result

    except FileNotFoundError as fnf_error:
        return {"error": str(fnf_error), "message": "Check the location of the file."}
    except ValueError as val_error:
        return {"error": str(val_error), "message": "Please provide an image with a clear face."}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}", "message": "Error while processing the image."}