import face_recognition as fr
import numpy as np
from myapp.models import Employe,Client
#settings.py
import os
from django.conf import settings
def checkfile(image):
    allowed_types = ['jpeg', 'png', 'gif', 'jpg', 'bmp', 'webp']
  
    if not image.name.lower().endswith(tuple(allowed_types)):
        return False
    return True

def is_ajax(request):
  return request.headers.get('x-requested-with') == 'XMLHttpRequest'

from itertools import chain


def get_encoded_faces():
    """
    This function loads all user 
    profile images and encodes their faces
    """
    # Retrieve all user profiles from the database
    employe_faces = Employe.objects.all()
    client_faces = Client.objects.all()

    # Chain the two querysets together
    qs = chain(employe_faces, client_faces)

    # Create a dictionary to hold the encoded face for each user
    encoded = {}
    encoding = None
    # Create an empty RGB image (3 channels: Red, Green, Blue) to save the face image
    face=np.zeros((480, 640, 3), dtype=np.uint8)
    
    for p in qs:
        # Initialize the encoding variable with None
        if checkfile(p.image) and p.is_image:
            
    
            image_path = p.image.path

            # Load the user's profile image using the corrected path
            face = fr.load_image_file(image_path)
            # ... rest of your code
      
       
       

        # Encode the face (if detected)
        face_encodings = fr.face_encodings(face)
        if len(face_encodings) > 0:
            encoding = face_encodings[0]
        else:
            print("No face found in the image")

        # Add the user's encoded face to the dictionary if encoding is not None
        if encoding is not None:
            encoded[p.user.username] = encoding

    # Return the dictionary of encoded faces
    print("encoded")
    return encoded


def classify_face(img):
    """
    This function takes an image as input and returns the name of the face it contains
    """
    # Load all the known faces and their encodings
    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    # Load the input image
    img_path = os.path.join(settings.MEDIA_ROOT, img)
    img = fr.load_image_file(img_path)
 
    try:
        # Find the locations of all faces in the input image
        face_locations = fr.face_locations(img)

        # Encode the faces in the input image
        unknown_face_encodings = fr.face_encodings(img, face_locations)

        # Identify the faces in the input image
        face_names = []
        for face_encoding in unknown_face_encodings:
            # Compare the encoding of the current face to the encodings of all known faces
            matches = fr.compare_faces(faces_encoded, face_encoding)

            # Find the known face with the closest encoding to the current face
            face_distances = fr.face_distance(faces_encoded, face_encoding)
            best_match_index = np.argmin(face_distances)

            # If the closest known face is a match for the current face, label the face with the known name
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            else:
                name = "Unknown"

            face_names.append(name)

        # Return the name of the first face in the input image
        return face_names[0]
    except:
        # If no faces are found in the input image or an error occurs, return False
        return False