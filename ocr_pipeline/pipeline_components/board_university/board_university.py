""" Extract Board's Name or University name from the certificates """

import json
import requests
from config import logger, university_api_colab

def extract_board_univer(ocr_text):
    """
    Extract the University name or Board name from the OCR text.
    Input: certificate's OCR text
    Output: university or board's name
    Error Info: Raise an error if spacy model doesn't recognise university or board name.
    """

    logger.info("------------------This is extract_board_univer function")

    # defining the api
    api_url = university_api_colab
    data = {
        "t": ocr_text
    }
    data = json.dumps(data)
    resp = requests.post(url = api_url, data = data)
    name_board_univer = resp.text
    
    logger.info("------------------This is extract_board_univer function respense: ", name_board_univer)
    return name_board_univer
