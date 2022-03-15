"""Certificate pre-processing such as rotation, crop, conversion etc"""

import numpy as np
from skimage.transform import hough_line, hough_line_peaks, rotate
from skimage.feature import canny
from skimage.io import imread, imsave
from skimage.color import rgb2gray
from scipy.stats import mode

def rotate_img(img_path):
    """
    Determine the angle of skewness.
    Input: image path
    Output: None
    """
    
    image = imread(img_path)
    image_grey = rgb2gray(image)
    edges = canny(image_grey)
    tested_angles = np.deg2rad(np.arange(60,120))
    h, theta, d = hough_line(edges, theta=tested_angles)
    _ , angles, _ = hough_line_peaks(h, theta, d)
    most_common_angle = mode(np.around(angles, decimals=2))[0]
    skew_angle = np.rad2deg(most_common_angle - np.pi/2)
    img_rotated = rotate(image, skew_angle)
    imsave(img_path, img_rotated)