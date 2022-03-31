"""Certificate post-processing such as ocr line coordinates correction, spell checker, etc"""

import hmni
from fuzzywuzzy import fuzz
from doctr.utils.visualization import visualize_page

#hmni for spellcorrection
matcher = hmni.Matcher(model='latin')

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


def savefig(img_path, result, doc):
    """
    savefig function will save the image with bounding boxes in processed folder
    """
    fig = visualize_page(result.pages[0].export(), doc[0], interactive=False)
    l = img_path.split("/")[-1]
    file_location = "data/processed/"+l
    fig.savefig(file_location)


