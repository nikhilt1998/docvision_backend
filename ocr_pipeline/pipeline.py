""" Initiate the data extraction pipeline. """

import os
import glob
from doctr.io import DocumentFile
from doctr.utils.visualization import visualize_page
from doctr.models import ocr_predictor
import json
import re
from pathlib import Path
import re
from redis import Redis


model = ocr_predictor(pretrained=True)

redis = Redis(host="redis")

def certificate_to_text(img_path, model):
    """
    Load and process the image to extract data using the OCR model.
    Input: Image path
    Output: Sorted and unsorted text bounding boxes boxes
    """

    # Load Image
    doc = DocumentFile.from_images(img_path)

    # Analyze
    result = model(doc)
    export = result.export()

    # Flatten the export
    page_words = [[word for block in page['blocks'] for line in block['lines'] 
                    for word in line['words']] for page in export['pages']]
    page_dims = [page['dimensions'] for page in export['pages']]

    # Get the coords in [xmin, ymin, xmax, ymax]
    words_abs_coords = [
        [[int(round(word['geometry'][0][0] * dims[1])), 
            int(round(word['geometry'][0][1] * dims[0])), 
            int(round(word['geometry'][1][0] * dims[1])), 
            int(round(word['geometry'][1][1] * dims[0])), 
            word['value']] for word in words]
        for words, dims in zip(page_words, page_dims)
    ]

    #list of bounding box around text from image
    bounding_boxes = words_abs_coords[0]

    # Sort Bounding Boxes based on ymin and xmin coords
    sorted_bounding_boxes = []

    # Sort bounding box Vertically  
    vert_bounding_boxes = sorted(bounding_boxes, key = lambda x: ( (x[1]+x[3])//2, (x[0]+x[2])//2))
    
    # Set the initial bound box and initial threshold value
    ini = vert_bounding_boxes[0]
    threshold_value_y = (ini[3] - ini[1])//2

    sorted_bounding_boxes.append([ini])

    # Sort the bounding boxes horizonatally to get lined text.
    for i in range(1, len(vert_bounding_boxes)):
        if( abs((vert_bounding_boxes[i][1] + vert_bounding_boxes[i][3]) - (ini[1] + ini[3]))//2 < threshold_value_y) :
            sorted_bounding_boxes[-1].append(vert_bounding_boxes[i])
            ini = vert_bounding_boxes[i]
        else:
            sorted_bounding_boxes[-1] = sorted(sorted_bounding_boxes[-1], key = lambda x: x[0])
            ini = vert_bounding_boxes[i]
            sorted_bounding_boxes.append([ini])

        threshold_value_y = (ini[3] - ini[1])//2

    sorted_bounding_boxes[-1] = sorted(sorted_bounding_boxes[-1], key = lambda x: x[0])

    return bounding_boxes, sorted_bounding_boxes

def pipeline(filename):
    """
    Pipeline function will initiatethe complete process of data extraction.
    Input: filename
    Output: success message
    """
    return
