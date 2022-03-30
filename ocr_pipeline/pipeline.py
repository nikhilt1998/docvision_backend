""" Initiate the data extraction pipeline. """

from re import sub
from unicodedata import category
import pipeline_components.board_university.board_university
import pipeline_components.degree_cert.degree_certi
import pipeline_components.grand_total_marks.grand_total_marks
import pipeline_components.sgpa_cgpa.sgpa_cgpa
import pipeline_components.subjects.subjects
import pipeline_components.year.year

import utils.certi_preprocess,utils.certi_postprocess,utils.ocr,utils.redis

from board_university import extract_board_univer
from degree_certi import extract_dc_details
from grand_total_marks import extract_total_marks
from sgpa_cgpa import extract_GPA
from subjects import extract_subjects
from year import extract_year

from certi_preprocess import deskew_img
from certi_postprocess import spellingCorrection,ocr_linecords_correction
from ocr import certificate_to_text,get_lined_text,get_spaced_text

from classify_certi import classify_certi

from doctr.models import ocr_predictor
import redis

from redis import Redis

# init redis
redis = Redis(host="redis")

# init DocTr model for OCR
model = ocr_predictor(pretrained=True)

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
    Pipeline function will initiate the complete process of data extraction.
    Input: filename
    Output: success message
    """
    filename = "data/uploaded_docs/" + filename
    new_filename = deskew_img(filename)
    new_filename = "data/deskewed_docs/" + new_filename

    # getting the text and bounding box around them.
    words_abs_coords = certificate_to_text(new_filename, model)

    # Spelling correction
    words_abs_coords = spellingCorrection(words_abs_coords)

    # Line correction
    bounding_boxes, sorted_bounding_boxes = ocr_linecords_correction(words_abs_coords)

    #ocr_text output
    ocr_text = get_spaced_text(sorted_bounding_boxes)

    #classify into categories
    categ = classify_certi(ocr_text)

    #json output to return
    pipeline_output = {}

    #class 1
    if categ == "dc":
      dc_out = extract_dc_details(ocr_text)
      pipeline_output['dc'] = dc_out

    #class 2
    elif categ == "gpa_pattern":
      board_univer_name = extract_board_univer(ocr_text)
      sgpa_cgpa = extract_GPA(sorted_bounding_boxes,bounding_boxes)
      subjects = extract_subjects(sorted_bounding_boxes)
      year = extract_year(ocr_text)

      pipeline_output['board_univer_name'] = board_univer_name
      pipeline_output['sgpa_cgpa'] = sgpa_cgpa
      pipeline_output['subjects'] = subjects
      pipeline_output['year'] = year
      
    #class 3
    else:
      board_univer_name = extract_board_univer(ocr_text)
      grand_total_marks = extract_total_marks(ocr_text)
      subjects = extract_subjects(sorted_bounding_boxes)
      year = extract_year(ocr_text)

      pipeline_output['board_univer_name'] = board_univer_name
      pipeline_output['grand_total_marks'] = grand_total_marks
      pipeline_output['subjects'] = subjects
      pipeline_output['year'] = year
    
    return pipeline_output
