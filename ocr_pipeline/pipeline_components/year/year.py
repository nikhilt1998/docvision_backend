""" Extract the certificate's issued year """

import re
from datetime import date
from transformers import pipeline

model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name)

def date_regex(date_str):
  """
  Extracting the year using regex.
  Input: answer from question and answering model.
  Output: Certificate issued year.
  """
  regex_dates = r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]|(?:jan|mar|may|jul|aug|oct|dec|january|march|may|july|august|october|december)))\1|(?:(?:29|30)(\/|-|\.)(?:0?[1,3-9]|1[0-2]|(?:jan|mar|apr|may|jun|jul|aug|sep|oct|nov|dec|january|march|april|may|june|july|august|september|october|november|december))\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)(?:0?2|(?:feb|february))\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9]|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|january|february|march|april|may|june|july|august|september))|(?:1[0-2]|(?:oct|nov|dec|october|november|december)))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$'

  x = re.search( regex_dates, date_str)

  cur_year = date.today().year%100
  cur_centuary = date.today().year//100

  if x != None:
    temp = date_str[x.end()-4:x.end()]
    try:
      temp1 = int(temp)
    except:
      temp1 = int(date_str[x.end()-2:x.end()])
      if  temp1 > cur_year:
        temp = ""+str((cur_centuary-1))+date_str[x.end()-2:x.end()]
      else:
        temp = ""+str((cur_centuary))+date_str[x.end()-2:x.end()]
    date_str = temp
  return date_str


def qna(question,context):
  """
  Extract the year using question and answering model.
  Input:  Question and OCR text for question and answering model.
  Output: answer for the question asked. 
  """
  qa_input = {
      'question': question,
      'context': context
  }
  res = nlp(qa_input)

  return res

def extract_year(ocr_text):
    """
    Extract the certificate issued year.
    Input: certificate's OCR text
    Output: extracted year
    """
    ans1 = qna('What is the examination month?',ocr_text)['answer'].lower()
    reg_response1 = date_regex(ans1)[-4:]
    ans2 = qna('What is certification issue year?',ocr_text)['answer'].lower()
    reg_response2 = date_regex(ans2)[-4:]

    # logging of no response and wrong response has to be handled : code has to be written and checked
    # logging for out of range year has to be done
    if reg_response1 == None or reg_response2 == None:
        year = "not found"

    
    if reg_response1.isdigit() and reg_response1.isdigit():
      if reg_response1 > reg_response2:
        year = reg_response1
      else:
        year = reg_response2
    else:
      if reg_response1.isdigit():
        year = reg_response1
      else:
        year = reg_response2

    return year

#sample check for rcoem univ and rgpv : passed both
# ocr_text='''RAJIV GANDHI PROUDYOGIKI VISHWAVIDYALAYA, BHOPAL
# (UNIVERSITY OF TECHNOLOGY OF MADHYA PRADESH)
# Accredited with A' grade by NAAC]
# REMSEDUEIOREMRUANON
# STATEMENT OF GRADE
# SR.NO. 3932623
# EXAMINATION DEC-2017
# B.Tech.,( Computer Science & Engineering) )
# ROLLNO. :0103CS171084
# NAME
# INSTT. Lakshmi Narain College of Technology, Bhopal
# SEMESTER F FIRST STATUS: Regular
# CREDITS
# SUBJECT SUBJECT NAME
# TOTAL CREDIT GRADE
# CODE
# CREDIT EARNED
# BT10010) Engineering Chemistry 4 4 B+
# BT1002(T] Mathematics-I 4 4 B+
# BI1003111 English 4 4 B
# BT1004(T] Basic Electrical & Electronics Engineering 4 4 B
# B1100510 Engineering Graphics 4 4 C+
# BT10011P] Engineering Chemistry 2 2 A+
# BI1003PJ English 2 2 A+
# BT1004/P] Basic Electrical & Electronics Engineering 2 2 A+
# BI1005P] Engineering Graphics 2 2 A+
# BT1006PI Workshop Practice 2 2 A+
# TOTAL 30 30
# RESULT - PASS SGPA: : 8.13 CGPA (As on Date): 8.13
# Issue Date 28/4/2018
# Prepared By Checked By Signature of Frincipar L 59-516 - Controller Akchph Dr. AK of Singh Examinations
# and Seal of Institution (RGPV, Bhopal)
# 0103 Lekshmi Narain Principat Ccilege el Technonogy 3932623
# BHOPAL'''

# print(extract_year(ocr_text))