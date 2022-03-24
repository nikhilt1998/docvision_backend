""" Extract Board's Name or University name from the certificates """

import json
import requests

def extract_board_univer(ocr_text):
    """
    Input: certificate's OCR text, OCR boxes
    Output: university or board's name
    """

    # defining the api
    api_url = "http://0ec6-104-198-50-1.ngrok.io/ner/"
    data = {
        "t": ocr_text
    }
    data = json.dumps(data)
    resp = requests.post(url = api_url, data = data)
    name_board_univer = resp.text

    return name_board_univer
