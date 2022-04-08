import re
import json
import spacy
from pathlib import Path



def extract_dc_details(ocr_text):
  """
  Extract the degree certifcate details from OCR text.
  Input: certificate's OCR text.
  Output: Degree certificate details in format
  """

  output_dir = Path("ner_dc")
  #requires spacyv2
  nlp_test = spacy.load(output_dir)
  doc = nlp_test(ocr_text)
  entities = [(ent.text, ent.label_) for ent in doc.ents]
  
  docx = {}
  docx['University'] = []
  docx['Branch'] = []
  docx['Result'] = []
  docx['USN'] = []
  for i in range(len(entities)):
    if (entities[i][1] == 'UNIVER'):
      docx['University'].append(entities[i][0])
    if (entities[i][1] == 'SUBJECT'):
      docx['Branch'].append(entities[i][0])
    if (entities[i][1] == 'RESULT'):
      docx['Result'].append(entities[i][0])
    if (entities[i][1] == 'USN'):
      docx['USN'].append(entities[i][0])
  
  #print(docx)
  # docx = json.dumps(docx, indent=2)    
  return docx


# ocr_text = """Sgegdas, 30088 Dgbomeab,temad
# VISVESVARAYA TECHNOLOGICAL UNIVERSITY, BELAGAVI
# KARNATAKA, INDIA
# Certifies that
# JAI GANESHMN
# 250.25005 eas aoeas0on
# a
# aoon enesots EFanVETEdO0 soncossphcos SD0E0
# sees SOEdAD Boon es0m sohcs0300hO
# has been duly admitted to the Degree of
# Bachelor of Engineering
# in recoguition of the fuilfilonent of reguirements
# bor the said degree
# 30cB0 530 X03
# University Seat Number : 4VV14CS036
# Daos
# Subject Computer Science d Engineering
# Berd
# First Class
# Class
# P 050008,00000 adadeoon BOOBO
# 018064
# Given under the seal of the University
# senpa
# A
# Belagavi
# -
# 6038
# ONDO6
# Date : MAR 18, 2019 VICE CHANCELLOR"""

# print(extract_dc_details(ocr_text))