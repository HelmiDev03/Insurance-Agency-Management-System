

# Create your tests here.
def checkfile(image):
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/jpg', 'image/bmp', 'image/webp']
  
    if image and image.content_type not in allowed_types:
        return False
    return True
        