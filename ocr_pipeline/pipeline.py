""" Initiate the data extraction pipeline. """

import sys

sys.path.insert(0,"ocr_pipeline/pipeline_components/board_university")
sys.path.insert(0,"ocr_pipeline/pipeline_components/degree_cert")
sys.path.insert(0,"ocr_pipeline/pipeline_components/grand_total_marks")
sys.path.insert(0,"ocr_pipeline/pipeline_components/sgpa_cgpa")
sys.path.insert(0,"ocr_pipeline/pipeline_components/subjects")
sys.path.insert(0,"ocr_pipeline/pipeline_components/year")
sys.path.insert(0,"utils")
sys.path.insert(0,"ocr_pipeline")

from board_university import extract_board_univer
# import pipeline_components.degree_cert.degree_certi
# import pipeline_components.grand_total_marks.grand_total_marks
# import pipeline_components.sgpa_cgpa.sgpa_cgpa
# import pipeline_components.subjects.subjects
# import pipeline_components.year.year

# import utils.certi_preprocess,utils.certi_postprocess,utils.ocr

# import board_university.extract_board_univer
from degree_certi import extract_dc_details
from grand_total_marks import extract_total_marks
from sgpa_cgpa import extract_GPA
from subjects import extract_subjects
from year import extract_year

from certi_preprocess import deskew_img
from certi_postprocess import spellingCorrection
from ocr import certificate_to_text,get_spaced_text,ocr_linecords_correction

from classify_certi import classify_certi_docs

from doctr.models import ocr_predictor
import redis
from utils.redis_fun import set_dict_redis,get_dict_redis

from redis import Redis
from config import logger

# init redis
redis = Redis(host="redis")

# init DocTr model for OCR
model = ocr_predictor(pretrained=True)


def pipeline(filename):
    """
    Pipeline function will initiate the complete process of data extraction.
    Input: filename
    Output: success message
    """
    key = filename.split('.')[0]

    # Updating up the redis directory 
    image_status = get_dict_redis("image_status")
    image_status[key]["Status"] = "Processing"
    set_dict_redis("image_status", image_status)

    logger.info("Image Status updated for "+ key)

    # skew detectition and correction 
    filename = "data/uploaded_docs/" + filename
    new_filename = deskew_img(filename)

    # getting the text and bounding box around them.
    words_abs_coords = certificate_to_text(new_filename, model)

    # Spelling correction
    words_abs_coords = spellingCorrection(words_abs_coords)

    # Line correction
    bounding_boxes, sorted_bounding_boxes = ocr_linecords_correction(words_abs_coords)

    #ocr_text output
    ocr_text = get_spaced_text(sorted_bounding_boxes)

    #classify into categories
    categ = classify_certi_docs(ocr_text)
    logger.info("------------------Certificate classified as ", categ)

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
    
    # Updating the redis directory
    image_status = get_dict_redis("image_status")
    state = image_status[key]
    state["Status"] = "Processed"
    state["Details"] = pipeline_output
    set_dict_redis("image_status", image_status)

    return pipeline_output
