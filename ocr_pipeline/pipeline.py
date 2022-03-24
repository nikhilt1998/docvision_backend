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
import hmni

print("This is the pipeline file")

# DocTr model for OCR
model = ocr_predictor(pretrained=True)

# init redis
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

    # saving the processed image
    savefig(img_path, result, doc)

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
        word['value'],
        word['confidence']] for word in words]
      for words, dims in zip(page_words, page_dims)
    ]

    return words_abs_coords


def savefig(img_path, result, doc):
    """
    savefig function will save the image with bounding boxes in processed folder
    """
    fig = visualize_page(result.pages[0].export(), doc[0], interactive=False)
    l = img_path.split("/")[-1]
    file_location = "data/processed/"+l
    fig.savefig(file_location)

def pipeline(filename):
    """
    Pipeline function will initiatethe complete process of data extraction.
    Input: filename
    Output: success message
    """

    # getting the text and bounding box around them.
    bounding_boxes, sorted_bounding_boxes = certificate_to_text("data/uploaded/"+filename, model)
    
    print(bounding_boxes)
    return 