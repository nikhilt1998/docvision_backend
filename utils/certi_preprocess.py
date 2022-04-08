"""Certificate pre-processing such as rotation, crop, conversion etc"""

import numpy as np
from skimage.transform import hough_line, hough_line_peaks, rotate
from skimage.feature import canny
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from scipy.stats import mode
import os

# def rotate_img(img_path):
#     """
#     Determine the angle of skewness.
#     Input: image path
#     Output: None
#     """
    
#     image = imread(img_path)
#     image_grey = rgb2gray(image)
#     edges = canny(image_grey)
#     tested_angles = np.deg2rad(np.arange(60,120))
#     h, theta, d = hough_line(edges, theta=tested_angles)
#     accum, angles, dists = hough_line_peaks(h, theta, d)
#     most_common_angle = mode(np.around(angles, decimals=2))[0]
#     skew_angle = np.rad2deg(most_common_angle - np.pi/2)
#     img_rotated = rotate(image, skew_angle)
#     imsave(img_path, img_rotated)

def skew_angle_hough_transform(image):
    """
    Caluculating the angle of the image.
    Input: Image.
    Output: Caluculated angle of the image.
    ///->Error Info: Raise an error if 
    """
    image_grey = rgb2gray(image)
    edges = canny(image_grey)
    tested_angles = np.deg2rad(np.arange(60,120))
    h, theta, d = hough_line(edges, theta=tested_angles)
    accum, angles, dists = hough_line_peaks(h, theta, d)
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
    image = imread(img_path)
    angle = skew_angle_hough_transform(image)
    print("Angle of rotation: ",angle[0])
    img_rotated = rotate(image, angle)

    path_to_rotatedImages = '../RotatedFolder'
    if not os.path.exists(path_to_rotatedImages):
      os.mkdir(path_to_rotatedImages)
    rotated_img_file_name = img_path.split('/')[-1].split('.')[0] + '_rotated_image.png'
    rotated_img_file_name = os.path.join(path_to_rotatedImages, rotated_img_file_name)
    print(rotated_img_file_name)
    imsave(rotated_img_file_name, img_rotated)
    rotated_img_file_name = img_path

    return rotated_img_file_name