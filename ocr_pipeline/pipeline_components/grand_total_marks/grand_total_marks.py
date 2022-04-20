""" Extract the total marks from the certificate """

from transformers import pipeline
from config import logger

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def qna(question,context):
  """
  Extract the grand total using question and answering model.
  Input:  Question and OCR text for question and answering model.
  Output: Answer for the question asked.
  """
  qa_input = {
      'question': question,
      'context': context
  }
  res = nlp(qa_input)

  return res

def preprocess_answer(text_str):
  """
  preprocess the answer received from qna to eliminate the unwanted characters/noise.
  Input: answer from qna model
  Output: preprocessed list of words 
  
  """
  unwantedChars = ['-', '.','*',':','/','\\']
  for char in unwantedChars:
    text_str = text_str.replace(char,"")
  text_str = text_str.replace("  "," ")
  # To remove noise in the answer (text might contain multiple lines) 
  sep = '\n'
  req_text = text_str.split(sep, 1)[0]
  list_of_words = req_text.split(" ")
  return list_of_words

def text2int(textnum):
    """
    Mapping the Grand Total text format to numerical format.
    Input: preprocessed answer string 
    Output: numeric format of grand total marks  
    """
    numwords={}
    textnum = textnum.lower()
    if not numwords:
      units = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
        "sixteen", "seventeen", "eighteen", "nineteen",
      ]

      tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

      scales = ["hundred", "thousand", "million", "billion", "trillion"]

      numwords["and"] = (1, 0)
      for idx, word in enumerate(units):    numwords[word] = (1, idx)
      for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
      for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

    current = result = 0
    for word in textnum.split():
        if word not in numwords:
          print("Garbage word found")
          continue

        scale, increment = numwords[word]
        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0
    if(result+current) == 0:  # gtotal not found
      return -1
    return result + current

def final_answer(list_of_words):
    """
    Return final grand total marks after the sanity checks.
    Input: list of words from preproccesed task.   
    Output: converted numeric formated grand total marks 
    """
    num_str_lst=[]
    digit = []

    for i in list_of_words:
      if(i.isdigit()):
        digit.append(i)
      else:
        num_str_lst.append(i)

    if len(digit)>1:
      if digit[0] == digit[1]:
        return digit[0] 
      else:
        return -1
    elif len(digit) == 1:
      return digit[0]
    else:
      num_str = " ".join(num_str_lst)
      return text2int(num_str)

def extract_total_marks(ocr_text):
    """
    Extract the grand total marks from the certificate.
    Input: certificate's OCR text.
    Output: extracted total marks.
    """
    ans1 = qna('grand total marks?',ocr_text)['answer']
    ans2 = qna('total marks obtained in words?',ocr_text)['answer']
    finaltext1 = preprocess_answer(ans1)
    finaltext2 = preprocess_answer(ans2)
    resp1 = final_answer(finaltext1)
    resp2 = final_answer(finaltext2)

    if(resp1 == -1 and resp2 == -1):
      looger.error("Total marks detected is invalid.")
      return "XXX"
    elif(resp1 == -1):
      temp_string = resp2
      try:
        temp_string = int(temp_string)
        if temp_string < 100:
          logger.error("Total marks detected is invalid.")
          resp2 = "XXX"
      except:
        logger.error("Total marks detected contains characters")
        resp2 = "XXX"
      return resp2
    
    temp_string = resp1
    try:
      temp_string = int(temp_string)
      if temp_string < 100:
        logger.error("Total marks detected is invalid.")
        resp1 = "XXX"
    except:
      logger.error("Total marks detected contains characters")
      resp1 = "XXX"
    return resp1

