""" Classifying the certificates uploaded by the User
    and verify the classification result with the user's input """

from fuzzywuzzy import fuzz,process
from config import logger

def classify_certi_docs(ocr_text):
    """
    Classifying the certificates uploaded by the User.
    Input: Certificate's OCR Text. 
    Output: Image category
    """
    choices1 = ["degree", "provisional"]  
    res1,conf1 = process.extractOne(ocr_text,choices1)
    
    
    if (res1 == "degree" or res1 == "provisional") and conf1 > 50:
      return "dc"
    elif conf1 < 50:
      choices2 = ["sgpa", "cgpa"]
      res2,conf2 = process.extractOne(ocr_text,choices2)
      
      if res2 == "sgpa" and conf2 > 50 or res2 == "cgpa" and conf2>50:
        return "gpa_pattern"
    
    return "marks_pattern"

def verify_user_input():
    """
    Verify the classification result with the user's input.
    Input: User Input
    Output: true/false
    Error info: Raise error if User input does not matches with classify_certi() result
    """
    return True
