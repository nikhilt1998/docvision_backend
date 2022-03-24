"""Certificate post-processing such as ocr line coordinates correction, spell checker, etc"""

import hmni
from fuzzywuzzy import fuzz

#hmni for spellcorrection
matcher = hmni.Matcher(model='latin')

def ocr_linecords_correction(words_abs_coords):
    # list of bounding box around text from image
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

def similarity_calculator(word1, word2, matcher):
    score_1 = fuzz.ratio(word1, word2) # score from fuzzywuzzy
    try:
      score_2 = matcher.similarity(word1, word2) # score from hmni
    except:
      score_2 = 0.0
    score_1 = score_1/100 # scaling [0, 1]
    
    score = 0.2*score_1 + 0.8*score_2 # customizing weights 
    return score


def spellingCorrection(words_abs_coords):
  lookupTable = ['TOTAL', 'ENGLISH', 'THEORY', 'PRACTICALS',
                 'West', 'Bengal', 'Secondary', 'SECONDARY', 
                 'Board', 'Results', 'EIGHTY', 'WORDS',
                 'SUBJECTS', 'FIRST', 'SECOND', 'MARKS']

  for words in range(len(words_abs_coords[0])):
    # print(words_abs_coords[0][words])
    if (words_abs_coords[0][words][-1] <= 0.10) and (len(words_abs_coords[0][words][-2]) <= 3): # In west bengal cert case
      words_abs_coords[0][words][-2] = ' ' # *(len(words_abs_coords[0][words][-2])) # regional languages 
    else:
      maxScoreTillNow = 0.0
      word1 = words_abs_coords[0][words][-2][:] # OCR words
      ocr_confidence = words_abs_coords[0][words][-1] # OCR word respective ocr_confidence
      
      flag = False # To check if word is found in Dictionary
      for word2 in lookupTable:
        currentScore = similarity_calculator(word1, word2, matcher) # Calculate HMNI score
        if currentScore > 0.60 and currentScore > maxScoreTillNow:
          if ocr_confidence < currentScore or (ocr_confidence - currentScore) < 0.07: # OCR co
            words_abs_coords[0][words][-2] = word2[:]
          maxScoreTillNow = currentScore
          flag = True
        
      if not flag:
        # decide to retain the misspelled word or make it to empty string
        # currently not making the word empty
        if ocr_confidence < 0.10:
          words_abs_coords[0][words][-2] = ' '
        else:
          words_abs_coords[0][words][-2] = word1[:]

  return words_abs_coords



"""def testOCRFunc(img_path):
  rot_img_path = rotate_img(img_path)
  # rot_img_path = "/content/rotated_image.png"
  words_abs_coords =  ocrFunc(rot_img_path, model)
  # Spelling correction
  words_abs_coords = spellingCorrection(words_abs_coords)
  # Line correction
  (text, crrt_bboxes, tableTextList) = lineCoordsCorrection(words_abs_coords)
  text = '\n'.join(tableTextList)
  return text, crrt_bboxes"""