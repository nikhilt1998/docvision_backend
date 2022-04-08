""" Extract the subjects mentioned in the certificate """

import json
import requests
import pandas as pd
import copy
from config import subjects_api_colab

def table_indices(crrt_bboxes, tabCord):
  """
  Identifying the starting and ending table row indices in the OCR text.
  Input: Sorted text bounding boxes and image table coordinates from table detection. 
  Output: List of table row indices of OCR text.
  """
  index_under_table = []
  xTabMin, yTabMin, xTabMax, yTabMax = tabCord

  for i in range(len(crrt_bboxes)):
    (xmin1, ymin1, xmax1, ymax1, word) = crrt_bboxes[i][0]
    (xmin2, ymin2, xmax2, ymax2, word) = crrt_bboxes[i][-1]
    xmid1 = (xmin1 + xmax1)//2
    ymid1 = (ymin1 + ymax1)//2

    xmid2 = (xmin2 + xmax2)//2
    ymid2 = (ymin2 + ymax2)//2

    if ((xTabMin < xmid1) and (yTabMin < ymid1) and (xTabMax > xmid1) and (yTabMax > ymid1)):
      if ((xTabMin < xmid2) and (yTabMin < ymid2) and (xTabMax > xmid2) and (yTabMax > ymid2)):
        index_under_table.append(i)
    
  return index_under_table


def columnSep(index_under_tablee, crrt_bboxes):
  """
  Seperating the words in the table text based upon which column it belongs to.
  Input: List of table row indices,Sorted bounding boxes. 
  Output: List of column seperated table text.
  """
  colSepLines = []

  for i in index_under_tablee:
    try:
      thres = (crrt_bboxes[i][0][2] - crrt_bboxes[i][0][0])/len(crrt_bboxes[i][0][-1])
    except ZeroDivisionError:
      thres = (crrt_bboxes[i][0][2] - crrt_bboxes[i][0][0])
      
    colSepWords = []
    wordsInACol = []
    wordsInACol.append(crrt_bboxes[i][0][:])
    colSepWords.append(wordsInACol[:])
    for j in range(1, len(crrt_bboxes[i])):
      (xmini, ymini, xmaxi, ymaxi, word)  = crrt_bboxes[i][j][:]
      if((xmini - colSepWords[-1][-1][2]) < thres):
        wordsInACol.append(crrt_bboxes[i][j][:])
        colSepWords[-1].append(crrt_bboxes[i][j][:])
      else:
        wordsInACol = []
        wordsInACol.append(crrt_bboxes[i][j][:])
        colSepWords.append(wordsInACol[:])
    colSepLines.append(colSepWords)

  return colSepLines
    


def modify_table(words_sep_cols):
  """
  Concatinating all the words in a column to a single word 
  and also merging the text bounding boxes of all the words in a column.
  Input: List of column seperated words. 
  Output: List of modified column seperated words.
  """
  table_lines = []
  for i in range(len(words_sep_cols)): # Line
    lines = []
    altCol = i
    for j in range(len(words_sep_cols[i])): # Column
      words_in_cols = []
      for k in range(len(words_sep_cols[i][j])): # Words in a Column
        if(k == 0):
          single_string = words_sep_cols[i][j][k][:]
          single_string.append(altCol)
        else:
          single_string[2] = words_sep_cols[i][j][k][2]
          single_string[3] = words_sep_cols[i][j][k][3]
          single_string[4] = single_string[4][:] + ' ' + words_sep_cols[i][j][k][4][:]

      words_in_cols.extend(single_string)
      lines.append(words_in_cols)
    table_lines.append(lines)
  return table_lines



def formTable(table_lines_parameter):
  """
  recreating the table structure using the column seperated words.
  Input: List of modified column seperated words. 
  Output: Table structured List of rows by column separated.
  """
  tableList = []
  table_lines = copy.deepcopy(table_lines_parameter)

  for row in range(len(table_lines)):
    for col in range(len(table_lines[row])):
      # First row in table
      if (row == 0):
        tableColumn = []
        tableColumn.append(table_lines[row][col])
        tableList.insert(len(tableList), tableColumn)
      else:
        xmid = (table_lines[row][col][0] + table_lines[row][col][2])/2
        flag = False
        for colTableList in range(len(tableList)):
          xTabMin, yTabMin, xTabMax, yTabMax, word, altCol = tableList[colTableList][-1]
          if ((xTabMin < xmid) and (xTabMax > xmid) and (row != altCol)):
            if(len(tableList[colTableList]) < row):
              tableColumn = [[-1, -1, -1, -1, ' ', -1]]*(row - len(tableList[colTableList]))
              tableList[colTableList].extend(tableColumn)
            
            table_lines[row][col][0] = min(xTabMin, table_lines[row][col][0])
            table_lines[row][col][2] = max(xTabMax, table_lines[row][col][2])

            tableList[colTableList].append(table_lines[row][col])
            flag = True
            break
          
        # Doesn't have any parent column cell 
        if not flag:
          innerFlag = False
          for colTableList in range(len(tableList)):
            xTabMin, yTabMin, xTabMax, yTabMax, word, altCol = tableList[colTableList][-1]
            if((xTabMin - xmid) > 0):
              tableColumn = [[-1, -1, -1, -1, ' ', -1]]*(row)
              tableColumn.append(table_lines[row][col])
              tableList.insert(colTableList, tableColumn)

              innerFlag = True
              break

          # For last column
          if not innerFlag:
            tableColumn = [[-1, -1, -1, -1, ' ', -1]]*(row)
            tableColumn.append(table_lines[row][col])
            tableList.insert(len(tableList), tableColumn)

  

  # To make height of all columns same
  rows = len(table_lines)
  for colTableList in range(len(tableList)):
    if(len(tableList[colTableList]) < rows):
      tableColumn = [[-1, -1, -1, -1, ' ', -1]]*(rows - len(tableList[colTableList]))
      tableList[colTableList].extend(tableColumn)
  
  return tableList

def storeOnlyValues(tableList):
  """
  Extract only text from table list
  Input: Table structured List of rows by column separated. 
  Output: Table text without Coordinates.
  """
  storeOnlyTableValue = []
  for col in range(len(tableList)):
    storeOnlyColumnValue = []
    for row in range(len(tableList[col])):
      storeOnlyColumnValue.append(tableList[col][row][-2])
    storeOnlyTableValue.append(storeOnlyColumnValue)

  return storeOnlyTableValue


def convertListToDataFrame(storeOnlyTableValue): 
  """
  Converting table list to pandas dataframe
  Input: Table text without Coordinates. 
  Output: Table text as DataFrame.
  """
  tableDataFrame = pd.DataFrame(storeOnlyTableValue)

  tableDataFrame = tableDataFrame.transpose()

  return tableDataFrame


def extract_subjects(crrt_bboxes):
    """
    Pipeline for Extracting the subjects and table data from OCR text
    Input: Sorted text bounding boxes.
    Output:Table text as HTML format
    """
     # defining the api
    api_url = subjects_api_colab
    data = {
        "image_path": "/content/drive/MyDrive/Infy_Assignment_Team_Anant/UNIVERSITIES_&_COLLEGES_MARKSHEETS/DocVisionData/Working Images/State-AP/AP-12.png",
    }
    data = json.dumps(data)
    resp = requests.post(url = api_url, data = data)
    tabCord = resp.text
    print(tabCord)
    tabCord = list(map(int,tabCord[1:-1].split(',')))

    index_under_tablee = table_indices(crrt_bboxes, tabCord)

    words_sep_cols = columnSep(index_under_tablee, crrt_bboxes)

    table_lines = modify_table(words_sep_cols)

    tableList = formTable(table_lines)

    storeOnlyTableValue = storeOnlyValues(tableList)

    tableDataFrame = convertListToDataFrame(storeOnlyTableValue)

    tableDataFrameHtml = tableDataFrame.to_html()
    tableDataFrameHtml = tableDataFrameHtml.replace("\n","")
    tableDataFrameHtml = tableDataFrameHtml.replace("\\","")
    

    return tableDataFrameHtml


# def extract_grades():
#     """
#     Input: certificate's OCR text, OCR boxes
#     Output: extracted grades list
#     """
#     return


"""crrt_bbox = [[[349, 45, 455, 59, '07/1806/E608863']],
 [[64, 58, 91, 78, 'SI.'],
  [91, 58, 123, 78, 'No.'],
  [134, 56, 239, 79, 'E608863']],
 [[89, 91, 196, 122, 'Board'],
  [202, 90, 243, 125, 'of'],
  [249, 90, 481, 125, 'Intermediate'],
  [493, 92, 745, 128, 'Education,A.P']],
 [[212, 126, 260, 150, 'Vidya'],
  [264, 126, 333, 149, 'Bhavan,'],
  [338, 128, 423, 150, 'Nampally,'],
  [428, 125, 522, 151, 'Hyderabad'],
  [524, 126, 544, 149, '-5'],
  [537, 125, 613, 148, '500001']],
 [[343, 324, 487, 341, 'INTERMEDIATE']],
 [[176, 344, 229, 366, 'PASS'],
  [232, 346, 358, 364, 'CERTIFICATE'],
  [361, 344, 406, 366, 'CUM'],
  [410, 346, 550, 364, 'MEMORANDUM'],
  [553, 345, 583, 365, 'OF'],
  [585, 346, 653, 365, 'MARKS']],
 [[102, 389, 140, 408, 'This'],
  [139, 390, 157, 409, 'is'],
  [155, 389, 177, 409, 'to'],
  [177, 390, 227, 409, 'certify'],
  [230, 391, 262, 406, 'that'],
  [294, 390, 369, 408, 'MANASA'],
  [370, 390, 490, 408, 'CHIMAKURTHI'],
  [643, 389, 719, 411, 'daughter']],
 [[102, 418, 125, 438, 'of'],
  [173, 420, 256, 438, 'VENKATA'],
  [257, 420, 354, 438, 'SUBBARAO'],
  [662, 421, 721, 436, 'bearing']],
 [[105, 449, 186, 466, 'Registered'],
  [186, 448, 216, 466, 'No.'],
  [234, 449, 321, 466, '050745734'],
  [411, 448, 441, 466, 'has'],
  [443, 449, 517, 468, 'appeared'],
  [517, 446, 538, 466, 'at'],
  [537, 448, 567, 466, 'the'],
  [569, 450, 667, 464, 'Intermediate'],
  [674, 450, 721, 465, 'Public']],
 [[104, 476, 201, 494, 'Examination'],
  [204, 478, 239, 492, 'held'],
  [241, 475, 260, 495, 'in'],
  [296, 476, 402, 494, 'MARCH-2005'],
  [444, 478, 474, 492, 'and'],
  [477, 479, 532, 494, 'passed'],
  [538, 475, 558, 495, 'in'],
  [561, 478, 610, 492, 'FIRST'],
  [613, 476, 689, 494, 'DIVISION']],
 [[103, 505, 138, 524, 'with'],
  [203, 505, 279, 522, 'ENGLISH'],
  [411, 508, 431, 522, 'as'],
  [431, 505, 460, 524, 'the'],
  [465, 506, 524, 521, 'Medium'],
  [525, 504, 547, 524, 'of'],
  [547, 505, 633, 522, 'Instruction.']],
 [[72, 549, 102, 564, 'The'],
  [105, 549, 173, 566, 'subjects'],
  [175, 546, 194, 566, 'in'],
  [197, 549, 243, 564, 'which'],
  [254, 546, 286, 565, 'she'],
  [304, 550, 336, 565, 'was'],
  [338, 548, 415, 565, 'examined'],
  [418, 549, 449, 564, 'and'],
  [450, 548, 479, 566, 'the'],
  [482, 550, 531, 564, 'marks'],
  [534, 550, 600, 564, 'awarded'],
  [602, 550, 631, 565, 'are'],
  [632, 550, 653, 566, 'as'],
  [656, 550, 710, 565, 'follows'],
  [713, 551, 721, 566, ':']],
 [[525, 571, 564, 586, 'LYear'], [664, 572, 711, 588, 'Year']],
 [[242, 585, 306, 604, 'Subject'],
  [474, 586, 542, 604, 'Maximum'],
  [559, 588, 600, 602, 'Marks'],
  [617, 589, 683, 602, 'Maximum'],
  [701, 589, 741, 602, 'Marks']],
 [[488, 604, 529, 619, 'Marks'],
  [551, 604, 607, 619, 'Secured'],
  [630, 604, 670, 619, 'Marks'],
  [693, 604, 749, 619, 'Secured']],
 [[77, 630, 111, 645, 'Part'],
  [114, 630, 134, 646, '1:'],
  [206, 636, 276, 654, 'ENGLISH'],
  [495, 636, 524, 655, '100'],
  [560, 636, 589, 655, '089'],
  [633, 636, 661, 655, '100'],
  [697, 636, 726, 655, '081']],
 [[75, 664, 107, 682, 'Part'],
  [104, 664, 134, 682, '2:'],
  [206, 666, 286, 684, 'SANSKRIT'],
  [495, 666, 524, 685, '100'],
  [560, 666, 590, 685, '092'],
  [633, 666, 661, 685, '100'],
  [697, 666, 727, 685, '095']],
 [[76, 692, 107, 711, 'Part'],
  [107, 696, 116, 708, '-'],
  [113, 694, 130, 710, '3:'],
  [127, 698, 134, 708, ':']],
 [[77, 711, 134, 726, 'Optional'], [138, 711, 195, 726, 'Subjects']],
 [[206, 725, 333, 739, 'MATHEMATICS-,'],
  [329, 724, 345, 740, 'A'],
  [494, 722, 524, 741, '075'],
  [561, 722, 592, 741, '072'],
  [632, 722, 661, 741, '075'],
  [697, 722, 727, 741, '075']],
 [[206, 755, 333, 769, 'MATHEMATICS-'],
  [329, 754, 344, 770, 'B'],
  [494, 752, 524, 771, '075'],
  [562, 752, 592, 771, '074'],
  [632, 752, 661, 771, '075'],
  [697, 752, 727, 771, '075']],
 [[206, 782, 274, 800, 'PHYSICS'],
  [494, 782, 524, 801, '060'],
  [562, 782, 591, 801, '056'],
  [632, 782, 661, 801, '060'],
  [697, 782, 727, 801, '049']],
 [[206, 815, 297, 829, 'CHEMISTRY'],
  [494, 812, 524, 831, '060'],
  [562, 812, 591, 831, '048'],
  [632, 812, 661, 831, '060'],
  [697, 812, 727, 831, '053']],
 [[206, 842, 274, 860, 'PHYSICS'],
  [276, 842, 366, 860, 'PRACTICAL'],
  [632, 842, 661, 861, '030'],
  [697, 842, 727, 861, '030']],
 [[206, 872, 298, 890, 'CHEMISTRY'],
  [298, 872, 388, 890, 'PRACTICAL'],
  [631, 872, 661, 891, '030'],
  [697, 872, 727, 891, '030']],
 [[74, 996, 114, 1015, 'Total'], [116, 999, 159, 1014, 'Marks']],
 [[73, 1012, 93, 1032, 'In'],
  [94, 1014, 146, 1032, 'Figures'],
  [232, 1008, 288, 1036, '919'],
  [382, 990, 468, 1041, '919']],
 [[73, 1049, 93, 1069, 'In'],
  [93, 1050, 138, 1069, 'words'],
  [141, 1056, 160, 1068, '1'],
  [185, 1056, 201, 1068, 'a'],
  [233, 1056, 394, 1075, 'NINE"ONE"NINE"']],
 [[74, 1090, 111, 1105, 'Date:'], [232, 1095, 319, 1112, '25-04-2005']],
 [[46, 1190, 176, 1225, 'VIGNANAIBHARAT'],
  [116, 1139, 326, 1188, 'GRauaujaynly'],
  [130, 1222, 207, 1250, 'CHIRA'],
  [131, 1169, 254, 1200, 'PRINCIPAL,'],
  [167, 1196, 292, 1231, 'THHIrdUNMPAnAGE'],
  [168, 1204, 175, 1218, ''],
  [197, 1222, 207, 1234, '1'],
  [215, 1220, 240, 1234, 'LITY'],
  [219, 1234, 233, 1245, 'E'],
  [277, 1172, 357, 1214, 'ghloste'],
  [341, 1128, 368, 1172, '6'],
  [354, 1110, 433, 1185, 'Sam'],
  [367, 1159, 455, 1185, 'CHIRALA'],
  [369, 1190, 394, 1211, 'DI'],
  [382, 1221, 407, 1235, 'DICA'],
  [473, 1221, 531, 1236, 'OBTAINED'],
  [531, 1220, 549, 1236, 'AT'],
  [547, 1221, 566, 1236, 'AN'],
  [565, 1222, 613, 1236, 'EARLIER'],
  [595, 1208, 659, 1221, 'Controller'],
  [613, 1222, 690, 1236, 'EXAMINATION'],
  [660, 1208, 762, 1221, 'ofExaminations'],
  [690, 1239, 761, 1256, '050745734']]]"""

# print(extract_subjects(crrt_bbox))