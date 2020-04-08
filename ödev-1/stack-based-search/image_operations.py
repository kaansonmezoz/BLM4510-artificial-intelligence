import cv2
import mimetypes
from PIL import Image


def read_image_rgb(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, image.shape[0], image.shape[1]

def is_file_image(file_path):
    mimetype = mimetypes.guess_type(file_path)[0]
    return mimetype is not None and "image" in mimetype

def show_image(image, node):    
    
    while node is not None:
        x = node.get_x()
        y = node.get_y()
        image[x][y][0] = 255
        image[x][y][1] = 255
        image[x][y][2] = 255
        node = node.get_parent()
        
    im2 = Image.fromarray(image)
    im2.show()
