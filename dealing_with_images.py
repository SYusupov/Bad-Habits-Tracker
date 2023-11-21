import os
import random
import glob
from PIL import Image

# putting images with appendages
def copy_resize_images_appendage(originDir, targetDir, size):
    """
    origingDir - the directory to copy images from
    targetDir - the directory to copy images to
    size - the """
    appendage = originDir[-1:]+'_'
    os.makedirs(targetDir, exist_ok=True)
    for fidx, filename in enumerate(glob.glob(originDir+'/*.jpg')):
        new_filename = appendage+str(fidx)+'.jpg'
        print('new filename', new_filename)
        im=Image.open(filename)
        im = im.resize((size, size))
        im.save(os.path.join(targetDir, os.path.basename(new_filename)), "JPEG")

def move_files_randomly(count_images, originDir, targetDir):
    """
    moving files from one directory to another
    count_images - number of images to move
    origingDir - the directory to move images from
    targetDir - the directory to move images to
    
    """
    os.makedirs(targetDir, exist_ok=True)
    for _ in range(count_images):
        filename = random.choice(os.listdir(originDir))
        os.rename(originDir+'/'+filename, targetDir+'/'+filename)
        
def delete_files_randomly(count_images, originDir):
    """
    randomly delete a specified number of images
    """
    for _ in range(count_images):
        filename = random.choice(os.listdir(originDir))
        print(filename)
        path = os.path.join(originDir, filename)
        os.remove(path)
        

def copy_resize_images(originDir, targetDir, size):
    """
    origingDir - the directory to copy images from
    targetDir - the directory to copy images to
    size - the """
    os.makedirs(targetDir, exist_ok=True)
    for filename in glob.glob(originDir+'/*.jpg'):
        print(filename)
        im=Image.open(filename)
        im = im.resize((size, size))
        im.save(os.path.join(targetDir, os.path.basename(filename)[:-4]+".jpg"), "JPEG")

def square_resize_image(image: Image, length: int) -> Image:
    """
    Resize an image to a square. Can make an image bigger to make it fit or smaller if it doesn't fit. It also crops
    part of the image.
    
    :param image: Image to resize.
    :param length: Width and height of the output image.
    :return: Return the resized image.
    """

    """
    Resizing strategy : 
     1) We resize the smallest side to the desired dimension (e.g. 1080)
     2) We crop the other side so as to make it fit with the same length as the smallest side (e.g. 1080)
    """
    if image.size[0] < image.size[1]:
        resized_image = image.resize((length, int(image.size[1] * (length / image.size[0]))))
        required_loss = (resized_image.size[1] - length)
        resized_image = resized_image.crop(
            box=(0, required_loss / 2, length, resized_image.size[1] - required_loss / 2))
        return resized_image
    else:
        resized_image = image.resize((int(image.size[0] * (length / image.size[1])), length))
        required_loss = resized_image.size[0] - length
        resized_image = resized_image.crop(
            box=(required_loss / 2, 0, resized_image.size[0] - required_loss / 2, length))
        return resized_image