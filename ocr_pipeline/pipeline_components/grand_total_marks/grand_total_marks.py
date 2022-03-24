""" Extract the total marks from the certificate """

from transformers import pipeline

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def qna(question,context):
  qa_input = {
      'question': question,
      'context': context
  }
  res = nlp(qa_input)

  return res

def preprocess(text_str):
  unwantedChars = ['-', '.','*',':','/','\\']
  for char in unwantedChars:
    text_str = text_str.replace(char,"")
  text_str = text_str.replace("  "," ")
  sep = '\n'
  stripped = text_str.split(sep, 1)[0]
  splt = stripped.split(" ")
  return splt

def text2int(textnum, numwords={}):
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

def convert(splt):
    num_str_lst=[]
    digit = []

    for i in splt:
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
    Input: certificate's OCR text
    Output: extracted total marks
    """
    ans1 = qna('grand total marks?',ocr_text)['answer']
    ans2 = qna('total marks obtained in words?',ocr_text)['answer']
    finaltext1 = preprocess(ans1)
    finaltext2 = preprocess(ans2)
    resp1 = convert(finaltext1)
    resp2 = convert(finaltext2)

    if(resp1 == -1 and resp2 == -1):
      return "do manual check"
    elif(resp1 == -1):
      return resp2
    
    return resp1

