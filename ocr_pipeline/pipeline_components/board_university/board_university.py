""" Extract Board's Name or University name from the certificates """

import json
import requests

def extract_board_univer(ocr_text):
    """
    Input: certificate's OCR text, OCR boxes
    Output: university or board's name
    """

    # defining the api
    api_url = "http://bb9f-35-225-67-160.ngrok.io/"
    data = {
        "t": ocr_text
    }
    data = json.dumps(data)
    resp = requests.post(url = api_url, data = data)
    name_board_univer = resp.text

    return name_board_univer
