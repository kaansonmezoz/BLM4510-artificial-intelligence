import cv2
import mimetypes


def read_image_rgb(file_path):
    image = cv2.imread(file_path, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image, image.shape[0], image.shape[1]

def is_file_image(file_path):
    mimetype = mimetypes.guess_type(file_path)[0]
    return mimetype is not None and "image" in mimetype