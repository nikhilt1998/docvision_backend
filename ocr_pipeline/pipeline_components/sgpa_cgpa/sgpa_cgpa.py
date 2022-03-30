""" Extract SGPA and CGPA from the certificates (if present)"""

import json

def getText(bboxes, crrt_bboxes, orientation):
  op = {}
  op["CGPA"] = ''
  op["SGPA"] = ''
  op["Orientation"] = ''


  if(orientation == 'H'):
    for i in range(len(crrt_bboxes)): # looping through all lines
      for j in range(len(crrt_bboxes[i])): # looping through all words in a line
        if( "CGPA" in crrt_bboxes[i][j][4].upper() or "SGPA" in crrt_bboxes[i][j][4].upper() or "GPA" in crrt_bboxes[i][j][4].upper() ):
          for k in range(j+1,len(crrt_bboxes[i])):
            try:
              if( "CGPA" in crrt_bboxes[i][k][4].upper() or "SGPA" in crrt_bboxes[i][k][4].upper() or "GPA" in crrt_bboxes[i][k][4].upper()): #(corner cases) SGPA ('OCR NOT RECOGNISED VALUE') CGPA 9.0 'or' SGPA 9.0 CGPA ('OCR NOT RECOGNISED VALUE')
                return
              
              num = float(crrt_bboxes[i][k][4].replace(":",""))
              substr = crrt_bboxes[i][j][4].upper().replace(":","")
              if(substr == "GPA"):
                substr = "SGPA"
              if(0<num<=10):
                op["Orientation"] = "horizontal"
                if(len(op[substr])==0):
                  op[substr] = str(num)
                break
              else:
                raise Exception()
            except:
              temp=0

  if(orientation == 'V'):

    for word in bboxes:
      if( "CGPA" in word[4].upper() or "SGPA" in word[4].upper() or "GPA" in word[4].upper() ):
        for number in bboxes:
          
          if(word[0] < (number[0]+number[2])//2 < word[2] and number[1] > word[1]):
            
            if( "CGPA" in number[4].upper() or "SGPA" in number[4].upper() or "GPA" in number[4].upper()):
              break
            try:
              num = float(number[4].replace(":",""))
              substr = word[4].upper().replace(":","")
              if(substr == "GPA"):
                substr = "SGPA"
              if(0<num<=10):
                op["Orientation"] = "Vertical"
                if(len(op[substr])==0):
                  op[substr] = str(num)
                break
              else:
                raise Exception()
            except:
              temp=0
  return op


def extract_GPA(crrt_bboxes, bboxes):
  grades = {}

  op = getText(bboxes,crrt_bboxes, 'H')
  if op is None:
    op = getText(bboxes,crrt_bboxes, 'V')
  
  for key, value in op.items():
    if(key != 'Orientation'):
      grades[key] = value

  return json.dumps(grades, indent=2)

#sample check for rgpv
# bboxes = [[146, 59, 190, 75, 'RAJIV', 0.9984028935432434], [192, 60, 254, 72, 'GANDHI', 0.9982848763465881], [256, 60, 361, 72, 'PROUDYOGIKI', 0.8560822606086731], [363, 59, 508, 75, 'VISHWAVIDYALAYA,', 0.99448162317276], [511, 61, 570, 74, 'BHOPAL', 0.8346990346908569], [195, 79, 276, 92, '(UNIVERSITY', 0.871345043182373], [276, 78, 295, 91, 'OF', 0.9997153878211975], [294, 79, 383, 91, 'TECHNOLOGY', 0.9983353018760681], [383, 79, 402, 92, 'OF', 0.9980573654174805], [402, 80, 459, 92, 'MADHYA', 0.9950711727142334], [460, 80, 522, 93, 'PRADESH)', 0.8717698454856873], [263, 96, 325, 109, 'Accredited', 0.9861159324645996], [327, 96, 351, 107, 'with', 0.9979041218757629], [351, 95, 368, 109, "'A'", 0.9415737390518188], [368, 96, 401, 109, 'grade', 0.9997225403785706], [401, 95, 417, 110, 'by', 0.9998922348022461], [418, 96, 455, 109, 'NAAC]', 0.9884759783744812], [239, 124, 320, 137, 'STATEMENT', 0.9991515874862671], [323, 124, 344, 137, 'OF', 0.9750619530677795], [345, 124, 394, 137, 'GRADE', 0.6381575465202332], [258, 150, 325, 160, 'EXAMINATION', 0.9952709674835205], [326, 150, 371, 160, 'DEC-2017', 0.9960196614265442], [216, 167, 260, 180, 'B.Tech.,(', 0.8858469724655151], [261, 168, 305, 179, 'Computer', 0.8946511149406433], [306, 168, 343, 178, 'Science', 0.4865056872367859], [342, 167, 352, 179, '&', 0.9995280504226685], [352, 168, 409, 180, 'Engineering)', 0.8123936057090759], [406, 168, 412, 179, ')', 0.9996662735939026], [394, 109, 545, 122, 'REMSEDOUEIOREMAUATON', 0.0008775657624937594], [443, 137, 464, 150, 'SR.', 0.972892165184021], [460, 137, 483, 150, 'NO.', 0.9940506219863892], [493, 130, 574, 149, '3932623', 0.996313214302063], [40, 181, 67, 191, 'ROLLI', 0.9491812586784363], [63, 181, 82, 191, 'NO.', 0.9756768345832825], [103, 179, 177, 191, ':0103CS171084', 0.5184766054153442], [40, 196, 69, 207, 'NAME', 0.9881102442741394], [39, 227, 71, 237, 'INSTT.', 0.9964110851287842], [39, 241, 94, 254, 'SEMESTER', 0.999400794506073], [103, 241, 112, 253, 'F', 0.9805768728256226], [108, 242, 139, 252, 'FIRST', 0.9935047030448914], [47, 278, 93, 287, 'SUBJECT', 0.9754716753959656], [56, 290, 85, 300, 'CODE', 0.8654484748840332], [103, 227, 145, 237, 'Lakshmi', 0.9543831944465637], [146, 227, 176, 237, 'Narain', 0.942679762840271], [178, 227, 212, 238, 'College', 0.9964073300361633], [212, 226, 224, 238, 'of', 0.9996920228004456], [224, 227, 276, 239, 'Technology,', 0.9900293350219727], [274, 227, 307, 238, 'Bhopal', 0.9922813177108765], [496, 239, 531, 248, 'STATUS:', 0.9974730610847473], [546, 239, 582, 249, 'Regular', 0.9524074792861938], [435, 265, 478, 275, 'CREDITS', 0.9988610148429871], [412, 283, 442, 293, 'TOTAL', 0.9998178482055664], [470, 283, 504, 293, 'CREDIT', 0.9975444674491882], [409, 295, 444, 305, 'CREDIT', 0.9991773366928101], [468, 295, 506, 305, 'EARNED', 0.8352540135383606], [421, 318, 429, 330, '4', 0.9999599456787109], [483, 318, 491, 330, '4', 0.9999732971191406], [420, 340, 429, 352, '4', 0.9664328694343567], [482, 340, 491, 352, '4', 0.9965631365776062], [421, 364, 429, 376, '4', 0.9996452927589417], [482, 363, 491, 376, '4', 0.9999895095825195], [420, 386, 429, 398, '4', 0.9999618530273438], [481, 386, 491, 398, '4', 0.9999837875366211], [420, 409, 429, 422, '4', 0.9999713897705078], [481, 409, 491, 422, '4', 0.9997444748878479], [419, 431, 429, 444, '2', 0.9998693466186523], [481, 431, 491, 444, '2', 0.9998798370361328], [419, 454, 429, 467, '2', 0.9997273087501526], [481, 455, 491, 467, '2', 0.9997435212135315], [419, 477, 429, 490, '2', 0.9996481537818909], [481, 477, 490, 490, '2', 0.9995813965797424], [419, 500, 429, 512, '2', 0.9995661973953247], [481, 500, 490, 513, '2', 0.9990277290344238], [419, 523, 429, 535, '2', 0.9996519684791565], [481, 523, 490, 536, '2', 0.9981687068939209], [213, 278, 260, 288, 'SUBJECT', 0.9990648627281189], [260, 278, 290, 288, 'NAME', 0.9217599034309387], [539, 284, 572, 293, 'GRADE', 0.9628110527992249], [549, 319, 563, 329, 'B+', 0.9970850348472595], [548, 341, 562, 352, 'B+', 0.999606192111969], [551, 364, 560, 376, 'B', 0.9590437412261963], [551, 386, 560, 398, 'B', 0.9980344772338867], [548, 410, 562, 421, 'C+', 0.9976357817649841], [547, 432, 562, 444, 'A+', 0.8650062084197998], [547, 455, 562, 466, 'A+', 0.9864503145217896], [547, 478, 562, 489, 'A+', 0.9901704788208008], [547, 501, 562, 512, 'A+', 0.9373887181282043], [546, 524, 561, 535, 'A+', 0.992691159248352], [49, 318, 97, 331, 'BT10010)', 0.20500193536281586], [108, 318, 162, 330, 'Engineering', 0.48455652594566345], [164, 319, 209, 329, 'Chemistry', 0.9883769750595093], [50, 342, 96, 352, 'B1100211', 0.28150081634521484], [108, 339, 172, 352, 'Mathematics-l', 0.35707545280456543], [50, 365, 96, 375, 'BI1003111', 0.28818845748901367], [108, 363, 142, 376, 'English', 0.9963626265525818], [49, 386, 96, 399, 'BT1004IT]', 0.32734233140945435], [108, 386, 134, 397, 'Basic', 0.9982458353042603], [136, 386, 177, 397, 'Electrical', 0.9640229344367981], [177, 385, 187, 398, '&', 0.999760627746582], [187, 385, 237, 398, 'Electronics', 0.9877362251281738], [237, 387, 291, 399, 'Engineering', 0.9971963167190552], [49, 411, 96, 421, 'B1100510', 0.09579872339963913], [107, 409, 162, 422, 'Engineering', 0.9911261200904846], [163, 409, 205, 422, 'Graphics', 0.9834848642349243], [48, 432, 96, 445, 'BT10011P]', 0.3630478084087372], [108, 431, 162, 444, 'Engineering', 0.9997653961181641], [163, 431, 209, 444, 'Chemistry', 0.9985448122024536], [49, 457, 96, 467, 'BI1003P', 0.17637436091899872], [108, 456, 142, 466, 'Engish', 0.5589919686317444], [48, 478, 96, 491, 'BT1004/P]', 0.43361055850982666], [107, 477, 134, 488, 'Basic', 0.999279260635376], [135, 477, 176, 488, 'Electrical', 0.9880895614624023], [176, 477, 186, 489, '&', 0.9996138215065002], [186, 477, 236, 489, 'Electronics', 0.9997101426124573], [236, 477, 291, 491, 'Engineering', 0.6140124797821045], [49, 503, 96, 513, 'BI1005P]', 0.14798398315906525], [106, 501, 162, 513, 'Engineering', 0.9978218078613281], [163, 500, 203, 513, 'Graphics', 0.9898362159729004], [48, 524, 96, 537, 'BT1006P]', 0.2194342464208603], [108, 524, 153, 535, 'Workshop', 0.9985057711601257], [155, 524, 192, 534, 'Practice', 0.9794740080833435], [240, 664, 274, 674, 'TOTAL', 0.9943673014640808], [249, 682, 280, 692, 'SGPA:', 0.9986762404441833], [277, 683, 283, 692, ':', 0.9938288331031799], [292, 681, 314, 691, '8.13', 0.9943805932998657], [416, 662, 430, 674, '30', 0.9998683929443359], [479, 662, 492, 674, '30', 0.9988381266593933], [37, 682, 76, 692, 'RESULT', 0.9947333931922913], [36, 702, 63, 713, 'Issue', 0.9963094592094421], [63, 702, 86, 713, 'Date', 0.9998073577880859], [103, 701, 149, 712, '28/4/2018', 0.7777008414268494], [37, 755, 82, 766, 'Prepared', 0.9931788444519043], [83, 754, 100, 768, 'By', 0.9999599456787109], [45, 791, 70, 804, '0103', 0.9988257884979248], [105, 681, 133, 691, 'PASS', 0.9976291060447693], [383, 682, 412, 692, 'CGPA', 0.999723494052887], [411, 681, 429, 695, '(As', 0.9917165637016296], [428, 682, 442, 694, 'on', 0.9977970719337463], [441, 682, 466, 695, 'Date)', 0.7341331243515015], [486, 680, 509, 693, '8.13', 0.9722623825073242], [348, 706, 364, 720, '-', 0.857749342918396], [320, 691, 440, 790, 'lgues', 0.02478153072297573], [450, 700, 553, 734, 'Axshiph', 0.040579721331596375], [467, 738, 481, 749, 'Dr.', 0.9782576560974121], [480, 737, 501, 750, 'AK:', 0.5764728784561157], [500, 738, 529, 751, 'Singh', 0.9992507100105286], [435, 754, 488, 767, 'Controller', 0.6518533825874329], [488, 754, 502, 767, 'of', 0.9896003007888794], [501, 754, 570, 767, 'Examinations', 0.9965194463729858], [464, 769, 501, 782, '(RGPV,', 0.9702996015548706], [503, 769, 542, 782, 'Bhopal)', 0.9976053237915039], [153, 755, 198, 766, 'Checked', 0.9987838268280029], [199, 754, 216, 768, 'By', 0.9969234466552734], [269, 755, 319, 767, 'Signature', 0.9966486692428589], [320, 754, 334, 767, 'of', 0.9909082651138306], [270, 770, 291, 780, 'and', 0.9983962774276733], [292, 770, 315, 780, 'Seal', 0.999456524848938], [316, 769, 330, 782, 'of', 0.999279260635376], [329, 769, 381, 781, 'Institution', 0.9962695240974426], [300, 782, 365, 798, 'Principat', 0.9357225894927979], [289, 798, 320, 812, 'Narain', 0.9982896447181702], [319, 796, 355, 812, 'Ccllege', 0.5908553004264832], [354, 796, 365, 809, 'el', 0.5696725249290466], [365, 795, 416, 808, 'Technonogy', 0.30393531918525696], [251, 800, 289, 816, 'Lekshmi', 0.6356356739997864], [313, 809, 356, 825, 'BHOPAL', 0.9951993227005005], [516, 793, 555, 802, '3932623', 0.9985700249671936]]
# crrt_bboxes = [[[146, 59, 190, 75, 'RAJIV'], [192, 60, 254, 72, 'GANDHI'], [256, 60, 361, 72, 'PROUDYOGIKI'], [363, 59, 508, 75, 'VISHWAVIDYALAYA,'], [511, 61, 570, 74, 'BHOPAL']], [[195, 79, 276, 92, '(UNIVERSITY'], [276, 78, 295, 91, 'OF'], [294, 79, 383, 91, 'TECHNOLOGY'], [383, 79, 402, 92, 'OF'], [402, 80, 459, 92, 'MADHYA'], [460, 80, 522, 93, 'PRADESH)']], [[263, 96, 325, 109, 'Accredited'], [327, 96, 351, 107, 'with'], [351, 95, 368, 109, "'A'"], [368, 96, 401, 109, 'grade'], [401, 95, 417, 110, 'by'], [418, 96, 455, 109, 'NAAC]']], [[394, 109, 545, 122, 'REMSEDOUEIOREMAUATON']], [[239, 124, 320, 137, 'STATEMENT'], [323, 124, 344, 137, 'OF'], [345, 124, 394, 137, 'GRADE']], [[443, 137, 464, 150, 'SR.'], [460, 137, 483, 150, 'NO.'], [493, 130, 574, 149, '3932623']], [[258, 150, 325, 160, 'EXAMINATION'], [326, 150, 371, 160, 'DEC-2017']], [[216, 167, 260, 180, 'B.Tech.,('], [261, 168, 305, 179, 'Computer'], [306, 168, 343, 178, 'Science'], [342, 167, 352, 179, '&'], [352, 168, 409, 180, 'Engineering)'], [406, 168, 412, 179, ')']], [[40, 181, 67, 191, 'ROLLI'], [63, 181, 82, 191, 'NO.'], [103, 179, 177, 191, ':0103CS171084']], [[40, 196, 69, 207, 'NAME']], [[39, 227, 71, 237, 'INSTT.'], [103, 227, 145, 237, 'Lakshmi'], [146, 227, 176, 237, 'Narain'], [178, 227, 212, 238, 'College'], [212, 226, 224, 238, 'of'], [224, 227, 276, 239, 'Technology,'], [274, 227, 307, 238, 'Bhopal']], [[39, 241, 94, 254, 'SEMESTER'], [103, 241, 112, 253, 'F'], [108, 242, 139, 252, 'FIRST'], [496, 239, 531, 248, 'STATUS:'], [546, 239, 582, 249, 'Regular']], [[435, 265, 478, 275, 'CREDITS']], [[47, 278, 93, 287, 'SUBJECT'], [213, 278, 260, 288, 'SUBJECT'], [260, 278, 290, 288, 'NAME']], [[412, 283, 442, 293, 'TOTAL'], [470, 283, 504, 293, 'CREDIT'], [539, 284, 572, 293, 'GRADE']], [[56, 290, 85, 300, 'CODE']], [[409, 295, 444, 305, 'CREDIT'], [468, 295, 506, 305, 'EARNED']], [[49, 318, 97, 331, 'BT10010)'], [108, 318, 162, 330, 'Engineering'], [164, 319, 209, 329, 'Chemistry'], [421, 318, 429, 330, '4'], [483, 318, 491, 330, '4'], [549, 319, 563, 329, 'B+']], [[50, 342, 96, 352, 'B1100211'], [108, 339, 172, 352, 'Mathematics-l'], [420, 340, 429, 352, '4'], [482, 340, 491, 352, '4'], [548, 341, 562, 352, 'B+']], [[50, 365, 96, 375, 'BI1003111'], [108, 363, 142, 376, 'English'], [421, 364, 429, 376, '4'], [482, 363, 491, 376, '4'], [551, 364, 560, 376, 'B']], [[49, 386, 96, 399, 'BT1004IT]'], [108, 386, 134, 397, 'Basic'], [136, 386, 177, 397, 'Electrical'], [177, 385, 187, 398, '&'], [187, 385, 237, 398, 'Electronics'], [237, 387, 291, 399, 'Engineering'], [420, 386, 429, 398, '4'], [481, 386, 491, 398, '4'], [551, 386, 560, 398, 'B']], [[49, 411, 96, 421, 'B1100510'], [107, 409, 162, 422, 'Engineering'], [163, 409, 205, 422, 'Graphics'], [420, 409, 429, 422, '4'], [481, 409, 491, 422, '4'], [548, 410, 562, 421, 'C+']], [[48, 432, 96, 445, 'BT10011P]'], [108, 431, 162, 444, 'Engineering'], [163, 431, 209, 444, 'Chemistry'], [419, 431, 429, 444, '2'], [481, 431, 491, 444, '2'], [547, 432, 562, 444, 'A+']], [[49, 457, 96, 467, 'BI1003P'], [108, 456, 142, 466, 'Engish'], [419, 454, 429, 467, '2'], [481, 455, 491, 467, '2'], [547, 455, 562, 466, 'A+']], [[48, 478, 96, 491, 'BT1004/P]'], [107, 477, 134, 488, 'Basic'], [135, 477, 176, 488, 'Electrical'], [176, 477, 186, 489, '&'], [186, 477, 236, 489, 'Electronics'], [236, 477, 291, 491, 'Engineering'], [419, 477, 429, 490, '2'], [481, 477, 490, 490, '2'], [547, 478, 562, 489, 'A+']], [[49, 503, 96, 513, 'BI1005P]'], [106, 501, 162, 513, 'Engineering'], [163, 500, 203, 513, 'Graphics'], [419, 500, 429, 512, '2'], [481, 500, 490, 513, '2'], [547, 501, 562, 512, 'A+']], [[48, 524, 96, 537, 'BT1006P]'], [108, 524, 153, 535, 'Workshop'], [155, 524, 192, 534, 'Practice'], [419, 523, 429, 535, '2'], [481, 523, 490, 536, '2'], [546, 524, 561, 535, 'A+']], [[240, 664, 274, 674, 'TOTAL'], [416, 662, 430, 674, '30'], [479, 662, 492, 674, '30']], [[37, 682, 76, 692, 'RESULT'], [105, 681, 133, 691, 'PASS'], [249, 682, 280, 692, 'SGPA:'], [277, 683, 283, 692, ':'], [292, 681, 314, 691, '8.13'], [383, 682, 412, 692, 'CGPA'], [411, 681, 429, 695, '(As'], [428, 682, 442, 694, 'on'], [441, 682, 466, 695, 'Date)'], [486, 680, 509, 693, '8.13']], [[36, 702, 63, 713, 'Issue'], [63, 702, 86, 713, 'Date'], [103, 701, 149, 712, '28/4/2018']], [[348, 706, 364, 720, '-'], [450, 700, 553, 734, 'Axshiph']], [[320, 691, 440, 790, 'lgues'], [467, 738, 481, 749, 'Dr.'], [480, 737, 501, 750, 'AK:'], [500, 738, 529, 751, 'Singh']], [[37, 755, 82, 766, 'Prepared'], [83, 754, 100, 768, 'By'], [153, 755, 198, 766, 'Checked'], [199, 754, 216, 768, 'By'], [269, 755, 319, 767, 'Signature'], [320, 754, 334, 767, 'of'], [435, 754, 488, 767, 'Controller'], [488, 754, 502, 767, 'of'], [501, 754, 570, 767, 'Examinations']], [[270, 770, 291, 780, 'and'], [292, 770, 315, 780, 'Seal'], [316, 769, 330, 782, 'of'], [329, 769, 381, 781, 'Institution'], [464, 769, 501, 782, '(RGPV,'], [503, 769, 542, 782, 'Bhopal)']], [[45, 791, 70, 804, '0103'], [300, 782, 365, 798, 'Principat'], [516, 793, 555, 802, '3932623']], [[251, 800, 289, 816, 'Lekshmi'], [289, 798, 320, 812, 'Narain'], [319, 796, 355, 812, 'Ccllege'], [354, 796, 365, 809, 'el'], [365, 795, 416, 808, 'Technonogy']], [[313, 809, 356, 825, 'BHOPAL']]]

#sample check for rcoem
# bboxes = [[1366, 128, 1437, 155, '(Estd.', 0.9865594506263733], [1438, 130, 1454, 155, ':', 0.9988971948623657], [1453, 123, 1521, 158, '1984)', 0.9969795346260071], [1304, 226, 1457, 260, '041594', 0.9722355008125305], [259, 171, 365, 212, 'SHRI', 0.9953701496124268], [376, 174, 685, 208, 'RAMDEOBABA', 0.9962590932846069], [693, 169, 902, 210, 'COLLEGE', 0.9994308352470398], [908, 167, 974, 210, 'OF', 0.9999289512634277], [983, 171, 1278, 205, 'ENGINEERING', 0.5045574307441711], [1284, 167, 1382, 208, 'AND', 0.9994441866874695], [567, 221, 879, 256, 'MANAGEMENT,', 0.6390572786331177], [892, 219, 1075, 253, 'NAGPUR', 0.9962077736854553], [404, 263, 525, 290, 'Ramdeo', 0.99873286485672], [530, 256, 621, 297, 'Tekdi,', 0.9996491074562073], [628, 258, 799, 292, 'Gittikhadan,', 0.9996338486671448], [807, 253, 884, 288, 'Katol', 0.6413545608520508], [890, 256, 979, 290, 'Road,', 0.9627642631530762], [983, 253, 1097, 295, 'Nagpur', 0.9994746446609497], [1102, 265, 1115, 283, '-', 0.9973294734954834], [1115, 253, 1179, 288, '440', 0.9998950958251953], [1177, 253, 1240, 288, '013', 0.9782716631889343], [450, 295, 508, 331, '(An', 0.9992878437042236], [509, 295, 700, 329, 'Autonomous', 0.9930995106697083], [706, 292, 850, 326, 'Institution', 0.9959474802017212], [857, 292, 951, 326, 'Under', 0.998238205909729], [956, 292, 1036, 326, 'UGC', 0.9970803260803223], [1033, 292, 1092, 326, 'Act', 0.8136473298072815], [1095, 290, 1185, 331, '1956)', 0.9980840086936951], [306, 338, 428, 372, 'Affiliated', 0.461145281791687], [428, 340, 460, 370, 'to', 0.9863525032997131], [461, 338, 617, 372, 'Rashtrasant', 0.9304683804512024], [620, 336, 734, 370, 'Unkaboji', 0.34485098719596863], [738, 336, 847, 370, 'Aaharaj', 0.2275596559047699], [850, 336, 950, 370, 'Nagpur', 0.8687860369682312], [951, 333, 1092, 368, 'Hribersity,', 0.2346930056810379], [1094, 331, 1195, 372, 'Nagpur', 0.9390467405319214], [1193, 333, 1264, 368, '(Estd.', 0.7655400037765503], [1265, 336, 1281, 358, ':', 0.9686621427536011], [1278, 331, 1347, 365, '1923)', 0.8995559215545654], [674, 429, 823, 461, 'SEMESTER', 0.9876881837844849], [828, 432, 924, 457, 'GRADE', 0.9991139769554138], [929, 429, 1007, 457, 'CARD', 0.9949288368225098], [237, 498, 389, 530, 'Programme:', 0.958002507686615], [412, 500, 474, 527, 'First', 0.857638955116272], [477, 498, 597, 532, 'Year(BE)', 0.9955922961235046], [239, 557, 312, 584, 'Name', 0.9962267875671387], [312, 553, 351, 589, 'of', 0.4587363302707672], [239, 594, 344, 621, 'Student:', 0.895756721496582], [239, 639, 338, 667, "Father's", 0.9988000392913818], [239, 676, 320, 701, 'Name:', 0.9996863007545471], [240, 721, 344, 747, "Mother's", 0.9429090619087219], [239, 756, 320, 783, 'Name:', 0.9993383884429932], [932, 573, 1031, 600, 'Student', 0.9985743165016174], [1033, 573, 1076, 600, 'ID:', 0.999261200428009], [932, 635, 1062, 667, 'Enrolment', 0.9990553259849548], [931, 669, 988, 703, 'No.:', 0.9973047375679016], [932, 735, 983, 763, 'Roll', 0.9987838268280029], [983, 735, 1039, 763, 'No.:', 0.9957347512245178], [932, 799, 1060, 831, 'Semester:', 0.9995375871658325], [1108, 801, 1169, 829, 'First', 0.9920192360877991], [240, 799, 400, 824, 'Examination:', 0.7622791528701782], [413, 799, 504, 824, 'Winter', 0.9990286827087402], [511, 797, 580, 824, '2017', 0.9999914169311523], [231, 909, 320, 936, 'Course', 0.9959142208099365], [325, 909, 389, 936, 'Code', 0.9994698762893677], [426, 909, 514, 936, 'Course', 0.9988981485366821], [519, 909, 593, 936, 'Name', 0.9997082352638245], [1091, 904, 1145, 938, 'N/M', 0.9994251132011414], [1203, 904, 1230, 936, 'C', 0.9988552927970886], [1294, 904, 1331, 934, 'Gr', 0.9999876022338867], [1397, 902, 1421, 934, 'P', 0.9998188018798828], [1203, 950, 1227, 982, '9', 0.9999351501464844], [1291, 950, 1331, 979, 'AA', 0.9930140376091003], [1392, 950, 1427, 979, '10', 0.9950408339500427], [1203, 991, 1227, 1025, '9', 0.9999599456787109], [1292, 993, 1331, 1023, 'BB', 0.9999189376831055], [1397, 991, 1421, 1023, '8', 0.9999523162841797], [1204, 1034, 1228, 1066, '3', 0.9999103546142578], [1292, 1034, 1331, 1064, 'AB', 0.9999103546142578], [1397, 1034, 1421, 1066, '9', 0.9999275207519531], [1204, 1075, 1228, 1107, '6', 0.999428927898407], [1292, 1078, 1332, 1105, 'AA', 0.9981887340545654], [1392, 1075, 1429, 1105, '10', 0.9983096122741699], [1204, 1116, 1228, 1148, '3', 0.9996815323829651], [1294, 1119, 1332, 1148, 'AA', 0.7284172773361206], [1393, 1119, 1429, 1148, '10', 0.9996157288551331], [1203, 1160, 1228, 1192, '4', 0.9985666871070862], [1292, 1160, 1332, 1190, 'AB', 0.9528544545173645], [1398, 1158, 1422, 1192, '9', 0.9998617172241211], [1204, 1203, 1228, 1235, '7', 0.9999246597290039], [1292, 1203, 1332, 1233, 'AA', 0.9986295700073242], [1393, 1203, 1429, 1233, '10', 0.9999322891235352], [1204, 1244, 1228, 1276, '2', 0.9998655319213867], [1294, 1247, 1332, 1274, 'AB', 0.999000072479248], [1398, 1242, 1422, 1276, '9', 0.9999666213989258], [1204, 1285, 1228, 1320, '2', 0.9999113082885742], [1294, 1288, 1332, 1317, 'BB', 0.9999351501464844], [1398, 1285, 1422, 1317, '8', 0.9999847412109375], [235, 957, 333, 982, 'MAT101', 0.9759755730628967], [235, 1000, 330, 1025, 'CHT101', 0.9991706609725952], [235, 1041, 332, 1069, 'CHP101', 0.9997692108154297], [235, 1085, 333, 1110, 'MET101', 0.9878097176551819], [237, 1126, 332, 1151, 'MEP101', 0.9998226165771484], [237, 1167, 335, 1194, 'HUT102', 0.9997454285621643], [237, 1210, 330, 1235, 'CET101', 0.9996462464332581], [237, 1251, 330, 1276, 'CEP101', 0.9998540878295898], [237, 1295, 327, 1320, 'INP102', 0.9894181489944458], [429, 957, 572, 989, 'Engineering', 0.7787896394729614], [577, 957, 732, 982, 'Mathematics', 0.9968069791793823], [734, 954, 750, 982, 'I', 0.9995385408401489], [429, 998, 572, 1030, 'Engineering', 0.8917561769485474], [578, 998, 700, 1025, 'Chemistry', 0.9992325901985168], [429, 1039, 572, 1073, 'Engineering', 0.9990382194519043], [578, 1041, 703, 1071, 'Chemistry', 0.999112069606781], [703, 1034, 754, 1069, 'Lab', 0.9643613696098328], [429, 1082, 573, 1114, 'Engineering', 0.9280104637145996], [580, 1082, 677, 1110, 'Drawing', 0.9998273849487305], [429, 1123, 573, 1155, 'Engineering', 0.9202491641044617], [580, 1126, 679, 1153, 'Drawing', 0.8771127462387085], [682, 1119, 732, 1153, 'Lab', 0.9995918869972229], [429, 1167, 504, 1194, 'Social', 0.9746315479278564], [508, 1167, 575, 1194, 'Skills', 0.999083936214447], [429, 1208, 573, 1240, 'Engineering', 0.9711489677429199], [578, 1208, 705, 1233, 'Mechanics', 0.9745107293128967], [431, 1249, 573, 1283, 'Engineering', 0.9992058873176575], [580, 1251, 705, 1276, 'Mechanics', 0.9978546500205994], [706, 1249, 748, 1276, 'lab', 0.9983686208724976], [432, 1295, 551, 1322, 'Workshop', 0.9704930186271667], [431, 1370, 545, 1395, 'Incentive', 0.9961028099060059], [549, 1368, 625, 1395, 'Grade', 0.9999351501464844], [629, 1368, 705, 1395, 'Points', 0.9973865151405334], [389, 1480, 452, 1514, 'ZEC', 0.38417890667915344], [399, 1518, 439, 1548, '45', 0.9992149472236633], [519, 1477, 567, 1514, 'EC', 0.9711318016052246], [522, 1518, 561, 1548, '45', 0.9981701374053955], [636, 1482, 693, 1509, 'ECP', 0.5068666934967041], [750, 1482, 825, 1509, 'SGPA', 0.9995757341384888], [636, 1518, 692, 1546, '419', 0.9999532699584961], [754, 1518, 815, 1546, '9.31', 0.9873538613319397], [1003, 1480, 1062, 1507, 'ZEC', 0.9836527109146118], [1009, 1511, 1054, 1548, '45', 0.9999809265136719], [1132, 1477, 1179, 1509, 'ZC', 0.5772033929824829], [1132, 1511, 1176, 1548, '45', 0.9995185136795044], [1246, 1475, 1308, 1509, 'ECP', 0.8868672251701355], [1361, 1477, 1438, 1505, 'CGPA', 0.9844382405281067], [1249, 1516, 1304, 1543, '419', 0.9999208450317383], [1366, 1511, 1430, 1546, '9.31', 0.9992125630378723], [258, 1502, 336, 1530, 'SGPA', 0.9993688464164734], [870, 1495, 950, 1530, 'CGPA', 0.9995156526565552], [240, 1623, 327, 1651, 'Result', 0.9992468953132629], [330, 1619, 351, 1655, ':', 0.9986724257469177], [360, 1619, 503, 1651, 'Successful', 0.9975859522819519], [239, 1703, 309, 1738, 'Date', 0.9828659892082214], [312, 1708, 327, 1735, ':', 0.9990448951721191], [362, 1703, 540, 1735, '20-Dec-2017', 0.7297585606575012], [242, 1763, 412, 1795, '1977647112', 0.9988791346549988], [1185, 1623, 1446, 1680, 'Mirroa..', 0.010714726522564888], [1105, 1699, 1241, 1731, 'Controller', 0.9993250370025635], [1243, 1699, 1278, 1733, 'of', 0.9999599456787109], [1278, 1699, 1459, 1731, 'Examinations', 0.9821661114692688], [762, 1692, 919, 1767, '(COE):', 0.7556073665618896], [769, 1772, 895, 1822, 'AGPUE', 0.5216682553291321], [131, 2002, 288, 2027, 'Abbreviations:', 0.9289571046829224], [290, 1998, 327, 2027, 'C:-', 0.8155661821365356], [325, 1998, 372, 2030, 'The', 0.9966087937355042], [370, 2000, 448, 2025, 'number', 0.9991296529769897], [448, 1998, 549, 2025, 'ofCredits', 0.9985914826393127], [553, 1998, 631, 2025, 'offered,', 0.9863778948783875], [633, 1996, 681, 2023, 'Gr:-', 0.976506233215332], [681, 1996, 753, 2023, 'Grades', 0.9927886724472046], [753, 1993, 823, 2021, 'earned', 0.9939871430397034], [823, 1993, 854, 2025, 'by', 0.999913215637207], [854, 1993, 934, 2021, 'student,', 0.9878813028335571], [934, 1991, 969, 2021, 'P:-', 0.989271879196167], [969, 1991, 1033, 2018, 'Grade', 0.9977841973304749], [1035, 1993, 1097, 2021, 'points', 0.9997892379760742], [1097, 1986, 1171, 2021, 'eamed', 0.9444326758384705], [1168, 1986, 1195, 2018, 'in', 0.9998092651367188], [1193, 1989, 1230, 2016, 'the', 0.9920466542243958], [1230, 1991, 1304, 2018, 'course,', 0.9207943081855774], [1304, 1986, 1344, 2016, 'N:-', 0.973666250705719], [1342, 1986, 1385, 2014, 'Not', 0.9987943172454834], [1384, 1984, 1411, 2016, 'in', 0.9660624265670776], [1411, 1984, 1454, 2014, 'first', 0.9910386800765991], [1454, 1986, 1538, 2014, 'Attempt,', 0.6055111885070801], [130, 2032, 173, 2059, 'M:-', 0.986552894115448], [173, 2032, 226, 2059, 'With', 0.9986791014671326], [226, 2030, 311, 2064, 'Makeup', 0.9975263476371765], [312, 2032, 444, 2057, 'Examination,', 0.9706369638442993], [447, 2030, 490, 2057, 'IG:-', 0.8852448463439941], [492, 2027, 629, 2059, 'Improvement', 0.9777969121932983], [629, 2027, 724, 2055, 'ofGrade,', 0.9991496801376343], [727, 2025, 842, 2053, 'EC=Eamed', 0.9121682047843933], [846, 2025, 924, 2053, 'Credits,', 0.8750115036964417], [926, 2023, 1004, 2050, 'SGPA:-', 0.9730193018913269], [1006, 2023, 1099, 2048, 'Semester', 0.9997473359107971], [1099, 2021, 1163, 2048, 'Grade', 0.9881875514984131], [1163, 2021, 1220, 2048, 'Point', 0.9997397065162659], [1220, 2023, 1305, 2050, 'Average', 0.9989476799964905], [1304, 2021, 1326, 2043, '==', 0.5443915128707886], [1324, 2016, 1469, 2048, '(ECP)/(EC),', 0.9345040321350098], [128, 2087, 186, 2121, 'THIS', 0.9849302768707275], [184, 2091, 311, 2117, 'STATEMENT', 0.9806302189826965], [308, 2089, 336, 2117, 'IS', 0.9910084009170532], [333, 2089, 383, 2117, 'NOT', 0.9998464584350586], [383, 2087, 450, 2114, 'VALID', 0.9997044205665588], [450, 2087, 535, 2112, 'UNLESS', 0.9987038373947144], [533, 2085, 562, 2114, 'IT', 0.9988352656364441], [561, 2085, 634, 2112, 'BEARS', 0.9994117617607117], [633, 2085, 681, 2112, 'THE', 0.9997482895851135], [681, 2085, 802, 2110, 'SIGNATURE', 0.8008919954299927], [802, 2082, 839, 2110, 'OR', 0.9991334676742554], [836, 2082, 958, 2110, 'SIGNATURE', 0.9996233582496643], [959, 2080, 1035, 2107, 'STAMP', 0.9996519684791565], [1030, 2080, 1065, 2107, 'OF', 0.9998245239257812], [1063, 2080, 1209, 2105, 'CONTROLLER', 0.999130129814148], [1208, 2075, 1243, 2105, 'OF', 0.9975292086601257], [1241, 2073, 1409, 2105, 'EXAMINATIONS', 0.46345779299736023], [1406, 2075, 1512, 2101, 'WITHTHE', 0.6667095422744751], [130, 2064, 211, 2089, 'CGPA:', 0.8593468070030212], [216, 2062, 330, 2089, 'Cumulative', 0.9981586933135986], [333, 2059, 397, 2087, 'Grade', 0.9518235921859741], [397, 2059, 453, 2087, 'Point', 0.9998178482055664], [453, 2062, 541, 2089, 'Average,', 0.7737201452255249], [546, 2059, 655, 2087, 'Equivalent', 0.9998207092285156], [653, 2055, 684, 2087, '%', 0.5676848888397217], [681, 2059, 709, 2087, 'as', 0.9999046325683594], [708, 2059, 746, 2089, 'per', 0.9990610480308533], [745, 2057, 798, 2085, 'table', 0.9998331069946289], [798, 2057, 847, 2085, 'over', 0.9999113082885742], [846, 2055, 894, 2082, 'leaf.', 0.9925520420074463], [131, 2121, 191, 2148, 'SEAL', 0.993024468421936], [189, 2121, 223, 2148, 'OF', 0.9988038539886475], [221, 2121, 324, 2146, 'COLLEGE', 0.995705783367157], [131, 2153, 195, 2187, '(This', 0.9998865127563477], [197, 2155, 308, 2180, 'Statement', 0.9985224008560181], [308, 2148, 335, 2183, 'is', 0.9914366602897644], [333, 2151, 415, 2185, 'subject', 0.9992192387580872], [415, 2151, 444, 2183, 'to', 0.9981820583343506], [442, 2148, 575, 2183, 'corrections,', 0.9498929977416992], [575, 2148, 602, 2180, 'if', 0.9970318078994751], [596, 2148, 660, 2183, 'any).', 0.9969766736030579]]
# crrt_bboxes = [[[1366, 128, 1437, 155, '(Estd.'], [1438, 130, 1454, 155, ':'], [1453, 123, 1521, 158, '1984)']], [[259, 171, 365, 212, 'SHRI'], [376, 174, 685, 208, 'RAMDEOBABA'], [693, 169, 902, 210, 'COLLEGE'], [908, 167, 974, 210, 'OF'], [983, 171, 1278, 205, 'ENGINEERING'], [1284, 167, 1382, 208, 'AND']], [[567, 221, 879, 256, 'MANAGEMENT,'], [892, 219, 1075, 253, 'NAGPUR'], [1304, 226, 1457, 260, '041594']], [[404, 263, 525, 290, 'Ramdeo'], [530, 256, 621, 297, 'Tekdi,'], [628, 258, 799, 292, 'Gittikhadan,'], [807, 253, 884, 288, 'Katol'], [890, 256, 979, 290, 'Road,'], [983, 253, 1097, 295, 'Nagpur'], [1102, 265, 1115, 283, '-'], [1115, 253, 1179, 288, '440'], [1177, 253, 1240, 288, '013']], [[450, 295, 508, 331, '(An'], [509, 295, 700, 329, 'Autonomous'], [706, 292, 850, 326, 'Institution'], [857, 292, 951, 326, 'Under'], [956, 292, 1036, 326, 'UGC'], [1033, 292, 1092, 326, 'Act'], [1095, 290, 1185, 331, '1956)']], [[306, 338, 428, 372, 'Affiliated'], [428, 340, 460, 370, 'to'], [461, 338, 617, 372, 'Rashtrasant'], [620, 336, 734, 370, 'Unkaboji'], [738, 336, 847, 370, 'Aaharaj'], [850, 336, 950, 370, 'Nagpur'], [951, 333, 1092, 368, 'Hribersity,'], [1094, 331, 1195, 372, 'Nagpur'], [1193, 333, 1264, 368, '(Estd.'], [1265, 336, 1281, 358, ':'], [1278, 331, 1347, 365, '1923)']], [[674, 429, 823, 461, 'SEMESTER'], [828, 432, 924, 457, 'GRADE'], [929, 429, 1007, 457, 'CARD']], [[237, 498, 389, 530, 'Programme:'], [412, 500, 474, 527, 'First'], [477, 498, 597, 532, 'Year(BE)']], [[239, 557, 312, 584, 'Name'], [312, 553, 351, 589, 'of'], [932, 573, 1031, 600, 'Student'], [1033, 573, 1076, 600, 'ID:']], [[239, 594, 344, 621, 'Student:']], [[239, 639, 338, 667, "Father's"], [932, 635, 1062, 667, 'Enrolment']], [[239, 676, 320, 701, 'Name:'], [931, 669, 988, 703, 'No.:']], [[240, 721, 344, 747, "Mother's"]], [[932, 735, 983, 763, 'Roll'], [983, 735, 1039, 763, 'No.:']], [[239, 756, 320, 783, 'Name:']], [[240, 799, 400, 824, 'Examination:'], [413, 799, 504, 824, 'Winter'], [511, 797, 580, 824, '2017'], [932, 799, 1060, 831, 'Semester:'], [1108, 801, 1169, 829, 'First']], [[231, 909, 320, 936, 'Course'], [325, 909, 389, 936, 'Code'], [426, 909, 514, 936, 'Course'], [519, 909, 593, 936, 'Name'], [1091, 904, 1145, 938, 'N/M'], [1203, 904, 1230, 936, 'C'], [1294, 904, 1331, 934, 'Gr'], [1397, 902, 1421, 934, 'P']], [[235, 957, 333, 982, 'MAT101'], [429, 957, 572, 989, 'Engineering'], [577, 957, 732, 982, 'Mathematics'], [734, 954, 750, 982, 'I'], [1203, 950, 1227, 982, '9'], [1291, 950, 1331, 979, 'AA'], [1392, 950, 1427, 979, '10']], [[235, 1000, 330, 1025, 'CHT101'], [429, 998, 572, 1030, 'Engineering'], [578, 998, 700, 1025, 'Chemistry'], [1203, 991, 1227, 1025, '9'], [1292, 993, 1331, 1023, 'BB'], [1397, 991, 1421, 1023, '8']], [[235, 1041, 332, 1069, 'CHP101'], [429, 1039, 572, 1073, 'Engineering'], [578, 1041, 703, 1071, 'Chemistry'], [703, 1034, 754, 1069, 'Lab'], [1204, 1034, 1228, 1066, '3'], [1292, 1034, 1331, 1064, 'AB'], [1397, 1034, 1421, 1066, '9']], [[235, 1085, 333, 1110, 'MET101'], [429, 1082, 573, 1114, 'Engineering'], [580, 1082, 677, 1110, 'Drawing'], [1204, 1075, 1228, 1107, '6'], [1292, 1078, 1332, 1105, 'AA'], [1392, 1075, 1429, 1105, '10']], [[237, 1126, 332, 1151, 'MEP101'], [429, 1123, 573, 1155, 'Engineering'], [580, 1126, 679, 1153, 'Drawing'], [682, 1119, 732, 1153, 'Lab'], [1204, 1116, 1228, 1148, '3'], [1294, 1119, 1332, 1148, 'AA'], [1393, 1119, 1429, 1148, '10']], [[237, 1167, 335, 1194, 'HUT102'], [429, 1167, 504, 1194, 'Social'], [508, 1167, 575, 1194, 'Skills'], [1203, 1160, 1228, 1192, '4'], [1292, 1160, 1332, 1190, 'AB'], [1398, 1158, 1422, 1192, '9']], [[237, 1210, 330, 1235, 'CET101'], [429, 1208, 573, 1240, 'Engineering'], [578, 1208, 705, 1233, 'Mechanics'], [1204, 1203, 1228, 1235, '7'], [1292, 1203, 1332, 1233, 'AA'], [1393, 1203, 1429, 1233, '10']], [[237, 1251, 330, 1276, 'CEP101'], [431, 1249, 573, 1283, 'Engineering'], [580, 1251, 705, 1276, 'Mechanics'], [706, 1249, 748, 1276, 'lab'], [1204, 1244, 1228, 1276, '2'], [1294, 1247, 1332, 1274, 'AB'], [1398, 1242, 1422, 1276, '9']], [[237, 1295, 327, 1320, 'INP102'], [432, 1295, 551, 1322, 'Workshop'], [1204, 1285, 1228, 1320, '2'], [1294, 1288, 1332, 1317, 'BB'], [1398, 1285, 1422, 1317, '8']], [[431, 1370, 545, 1395, 'Incentive'], [549, 1368, 625, 1395, 'Grade'], [629, 1368, 705, 1395, 'Points']], [[258, 1502, 336, 1530, 'SGPA'], [389, 1480, 452, 1514, 'ZEC'], [399, 1518, 439, 1548, '45'], [519, 1477, 567, 1514, 'EC'], [522, 1518, 561, 1548, '45'], [636, 1482, 693, 1509, 'ECP'], [636, 1518, 692, 1546, '419'], [750, 1482, 825, 1509, 'SGPA'], [754, 1518, 815, 1546, '9.31'], [870, 1495, 950, 1530, 'CGPA'], [1003, 1480, 1062, 1507, 'ZEC'], [1009, 1511, 1054, 1548, '45'], [1132, 1477, 1179, 1509, 'ZC'], [1132, 1511, 1176, 1548, '45'], [1246, 1475, 1308, 1509, 'ECP'], [1249, 1516, 1304, 1543, '419'], [1361, 1477, 1438, 1505, 'CGPA'], [1366, 1511, 1430, 1546, '9.31']], [[240, 1623, 327, 1651, 'Result'], [330, 1619, 351, 1655, ':'], [360, 1619, 503, 1651, 'Successful'], [1185, 1623, 1446, 1680, 'Mirroa..']], [[239, 1703, 309, 1738, 'Date'], [312, 1708, 327, 1735, ':'], [362, 1703, 540, 1735, '20-Dec-2017'], [762, 1692, 919, 1767, '(COE):'], [1105, 1699, 1241, 1731, 'Controller'], [1243, 1699, 1278, 1733, 'of'], [1278, 1699, 1459, 1731, 'Examinations']], [[242, 1763, 412, 1795, '1977647112']], [[769, 1772, 895, 1822, 'AGPUE']], [[131, 2002, 288, 2027, 'Abbreviations:'], [290, 1998, 327, 2027, 'C:-'], [325, 1998, 372, 2030, 'The'], [370, 2000, 448, 2025, 'number'], [448, 1998, 549, 2025, 'ofCredits'], [553, 1998, 631, 2025, 'offered,'], [633, 1996, 681, 2023, 'Gr:-'], [681, 1996, 753, 2023, 'Grades'], [753, 1993, 823, 2021, 'earned'], [823, 1993, 854, 2025, 'by'], [854, 1993, 934, 2021, 'student,'], [934, 1991, 969, 2021, 'P:-'], [969, 1991, 1033, 2018, 'Grade'], [1035, 1993, 1097, 2021, 'points'], [1097, 1986, 1171, 2021, 'eamed'], [1168, 1986, 1195, 2018, 'in'], [1193, 1989, 1230, 2016, 'the'], [1230, 1991, 1304, 2018, 'course,'], [1304, 1986, 1344, 2016, 'N:-'], [1342, 1986, 1385, 2014, 'Not'], [1384, 1984, 1411, 2016, 'in'], [1411, 1984, 1454, 2014, 'first'], [1454, 1986, 1538, 2014, 'Attempt,']], [[130, 2032, 173, 2059, 'M:-'], [173, 2032, 226, 2059, 'With'], [226, 2030, 311, 2064, 'Makeup'], [312, 2032, 444, 2057, 'Examination,'], [447, 2030, 490, 2057, 'IG:-'], [492, 2027, 629, 2059, 'Improvement'], [629, 2027, 724, 2055, 'ofGrade,'], [727, 2025, 842, 2053, 'EC=Eamed'], [846, 2025, 924, 2053, 'Credits,'], [926, 2023, 1004, 2050, 'SGPA:-'], [1006, 2023, 1099, 2048, 'Semester'], [1099, 2021, 1163, 2048, 'Grade'], [1163, 2021, 1220, 2048, 'Point'], [1220, 2023, 1305, 2050, 'Average'], [1304, 2021, 1326, 2043, '=='], [1324, 2016, 1469, 2048, '(ECP)/(EC),']], [[128, 2087, 186, 2121, 'THIS'], [130, 2064, 211, 2089, 'CGPA:'], [184, 2091, 311, 2117, 'STATEMENT'], [216, 2062, 330, 2089, 'Cumulative'], [308, 2089, 336, 2117, 'IS'], [333, 2059, 397, 2087, 'Grade'], [333, 2089, 383, 2117, 'NOT'], [383, 2087, 450, 2114, 'VALID'], [397, 2059, 453, 2087, 'Point'], [450, 2087, 535, 2112, 'UNLESS'], [453, 2062, 541, 2089, 'Average,'], [533, 2085, 562, 2114, 'IT'], [546, 2059, 655, 2087, 'Equivalent'], [561, 2085, 634, 2112, 'BEARS'], [633, 2085, 681, 2112, 'THE'], [653, 2055, 684, 2087, '%'], [681, 2059, 709, 2087, 'as'], [681, 2085, 802, 2110, 'SIGNATURE'], [708, 2059, 746, 2089, 'per'], [745, 2057, 798, 2085, 'table'], [798, 2057, 847, 2085, 'over'], [802, 2082, 839, 2110, 'OR'], [836, 2082, 958, 2110, 'SIGNATURE'], [846, 2055, 894, 2082, 'leaf.'], [959, 2080, 1035, 2107, 'STAMP'], [1030, 2080, 1065, 2107, 'OF'], [1063, 2080, 1209, 2105, 'CONTROLLER'], [1208, 2075, 1243, 2105, 'OF'], [1241, 2073, 1409, 2105, 'EXAMINATIONS'], [1406, 2075, 1512, 2101, 'WITHTHE']], [[131, 2121, 191, 2148, 'SEAL'], [189, 2121, 223, 2148, 'OF'], [221, 2121, 324, 2146, 'COLLEGE']], [[131, 2153, 195, 2187, '(This'], [197, 2155, 308, 2180, 'Statement'], [308, 2148, 335, 2183, 'is'], [333, 2151, 415, 2185, 'subject'], [415, 2151, 444, 2183, 'to'], [442, 2148, 575, 2183, 'corrections,'], [575, 2148, 602, 2180, 'if'], [596, 2148, 660, 2183, 'any).']]]

# print(extract_GPA(crrt_bboxes, bboxes))