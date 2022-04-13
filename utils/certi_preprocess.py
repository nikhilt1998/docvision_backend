"""Certificate pre-processing such as rotation, crop, conversion etc"""

import numpy as np
from skimage.transform import hough_line, hough_line_peaks, rotate
from skimage.feature import canny
from skimage.io import imread, imsave
from skimage.color import rgb2gray, rgba2rgb
from scipy.stats import mode
import os
from PIL import Image
from config import logger


def skew_angle_hough_transform(image):
    """
    Caluculating the angle of the image.
    Input: Image.
    Output: Caluculated angle of the image.
    ///->Error Info: Raise an error if 
    """
    image_grey = rgb2gray(rgba2rgb(image))
    edges = canny(image_grey)
    tested_angles = np.deg2rad(np.arange(60,120))
    h, theta, d = hough_line(edges, theta=tested_angles)
    _ , angles, _ = hough_line_peaks(h, theta, d)
    most_common_angle = mode(np.around(angles, decimals=2))[0]
    skew_angle = np.rad2deg(most_common_angle - np.pi/2)
    return skew_angle
    
def deskew_img(img_path):
    """
    deskewing the image for OCR to extract text.
    Input:  path of the image.
    Output: deskewed image.
    ///->Error Info: Raise an error if 
    """
    try:
        image = imread(img_path)
        angle = skew_angle_hough_transform(image)
        logger.debug("Angle of rotation: "+ str(angle[0]))
        Original_Image = Image.open(img_path)
        image = Original_Image.rotate(angle[0])
    except:
        logger.error("Deskew failed for " + str(img_path) + ", pipeline continue with skewed image.") 

    path_to_rotatedImages = 'data/deskewed_docs'

    rotated_img_file_name = img_path.split('/')[-1].split('.')[0] + '_rotated_image.png'
    rotated_img_file_name = os.path.join(path_to_rotatedImages, rotated_img_file_name)

    image.save(rotated_img_file_name)
    rotated_img_file_name = img_path

    logger.info("Image saved in deskew folder.")

    return rotated_img_file_name
