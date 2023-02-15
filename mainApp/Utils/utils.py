from Levenshtein import jaro
import re
from collections import Counter
from datetime import date, datetime
from pythainlp.util import thai_strftime
# from pythainlp.spell import NorvigSpellChecker
# from pythainlp.tokenize import sent_tokenize
# import sys
# adding Folder_2 to the system path
# from readDictFile import readDictTuple

current_year = date.today().year

def similarityListWord(t1: str, lst: list):
  res_sim = [jaro(t1, ele) for ele in lst]
  max_res_sim = max(res_sim)
  return max_res_sim, res_sim.index(max_res_sim)

def binary_search(lst: list, x: any) -> any :
  low = 0
  high = len(lst) - 1
  mid = 0

  while low <= high:
    mid = (high + low) // 2
    # If x is greater, ignore left half
    if lst[mid] < x:
      low = mid + 1
    # If x is smaller, ignore right half
    elif lst[mid] > x:
      high = mid - 1
    # means x is present at mid
    else:
      return mid
  # If we reach here, then the element was not present
  return -1

def regexSearch(s: str, pattern: str) -> str :
  serach_num = re.search(pattern, s)
  if serach_num:
    result = serach_num.group()
  else:
    result = ''
  return result

def regexFindAll(s: str, pattern: str) -> list:
  regex = re.compile(pattern)
  serach_Num = regex.findall(s)
  return serach_Num

def regexSub(s: str, pattern: str) -> list:
  regex = re.sub(pattern, "", s)
  return regex

'''
def spellingCorrecting(s: str) -> str:
  res = ''
  word_token = sent_tokenize(s, engine='whitespace')
  len_word_token =len(word_token)
  custom_dict = readDictTuple(filename = '../myDictionary/tncwordfreq-201712.json')
  # custom_dict = readDictList(filename='../myDictionary/bigthai.txt')
  norvig = NorvigSpellChecker(custom_dict=custom_dict, min_freq = 2, max_len = 40)
  for idx in range(len_word_token):
    res = res + norvig.correct(word = word_token[idx])
    if idx != (len_word_token-1):
      res = res + ' '
  return res
'''

def candidateFromList(lst: list):
  occurence_count = Counter(lst)
  return occurence_count.most_common(1)[0][0]

def normalizeDate(txt: str):
  list_of_month = { "มกราคม": 1, 
                    "กุมภาพันธ์": 2, 
                    "มีนาคม": 3, 
                    "เมษายน": 4, 
                    "พฤษภาคม": 5,
                    "มิถุนายน": 6, 
                    "กรกฎาคม": 7, 
                    "สิงหาคม": 8, 
                    "กันยายน": 9, 
                    "ตุลาคม": 10, 
                    "พฤศจิกายน": 11, 
                    "ธันวาคม": 12,
                    "ม.ค.": 1,
                    "ก.พ.": 2,
                    "มี.ค.": 3,
                    "เม.ย.": 4,
                    "พ.ค.": 5,
                    "มิ.ย.": 6,
                    "ก.ค.": 7,
                    "ส.ค.": 8,
                    "ก.ย.": 9,
                    "ต.ค.": 10,
                    "พ.ย.": 11,
                    "ธ.ค.": 12,}
  pattern1 = r'\d{1,2}[\.\-/ ]\d{1,2}[\.\-/ ]\d{4}'
  pattern2 = r'\d{4}[\.\-/ ]\d{1,2}[\.\-/ ]\d{1,2}'
  pattern3 = r'\d{1,2}[\.\-/ ]\d{1,2}[\.\-/ ]\d{2}'
  try:
    if re.match(pattern1, txt): # A.D.
      split_date = re.split(r'[\.\-/ ]', txt)
      split_date = [int(ele) for ele in split_date]
      if split_date[2] <= current_year:
        return datetime(year=split_date[2], month=split_date[1],\
                        day=split_date[0], hour=0, minute=0,\
                        second=0, microsecond=0)
      else: # B.E
        return datetime(year=split_date[2]-543, month=split_date[1],\
                        day=split_date[0], hour=0, minute=0,\
                        second=0, microsecond=0)      
    elif re.match(pattern2, txt):  # A.D.
      split_date = re.split(r'[\.\-/ ]', txt)
      split_date = [int(ele) for ele in split_date]
      if split_date[0] <= current_year:
        return datetime(year=split_date[0], month=split_date[1],\
                        day=split_date[2], hour=0, minute=0,\
                        second=0, microsecond=0)
      else:  # B.E
        return datetime(year=split_date[0]-543, month=split_date[1],\
                        day=split_date[2], hour=0, minute=0,\
                        second=0, microsecond=0)    
    elif re.match(pattern3, txt):
      split_date = re.split(r'[\.\-/ ]', txt)
      split_date = [int(ele) for ele in split_date]
      if (split_date[0] >= 56 and split_date[0] <= (current_year+543)%100) and (split_date[2] >= 1 and split_date[0] <= 31): # yy/mm/dd
        return datetime(year=(2500+split_date[0])-543, month=split_date[1],\
                        day=split_date[2], hour=0, minute=0,\
                        second=0, microsecond=0)   
      elif (split_date[2] >= 56 and split_date[2] <= (current_year+543)%100) and (split_date[0] >= 1 and split_date[0] <= 31): # dd/mm/yy
        return datetime(year=(2500+split_date[2])-543, month=split_date[1],\
                        day=split_date[0], hour=0, minute=0,\
                        second=0, microsecond=0)   
    else:
      split_date = re.split(r'[\-/ ]', txt)
      split_date[0] = int(re.sub(r'[a-zA-Z\u0E01-\u0E4F]','',split_date[0]))
      split_date[2] = int(re.sub(r'[a-zA-Z\u0E01-\u0E4F]','',split_date[2]))
      
      if split_date[2] >= current_year : # B.E
        return datetime(year=split_date[2]-543, month=list_of_month[split_date[1]],\
                        day=split_date[0], hour=0, minute=0,\
                        second=0, microsecond=0)   
      else: # A.D.
        if split_date[2] <= (current_year+543)%100:
          return datetime(year=(2500+split_date[2])-543, month=list_of_month[split_date[1]],\
                        day=split_date[0], hour=0, minute=0,\
                        second=0, microsecond=0)   
  except:
    return None

def handlePriceAndQTY(txt: str):
  try:
    seacrh_Invalid_AbleSolve = re.search(",\d{2}$",txt)
    if seacrh_Invalid_AbleSolve:
      idx_invalid = seacrh_Invalid_AbleSolve.start()
      txt = txt[:idx_invalid] + '.' + txt[idx_invalid+1:]
      txt = re.sub(',', '', txt)
    string = re.sub(',', '', txt)
    if not(re.search(".",txt)):
      return int(string) 
    return float(string) 
  except:
    return None


def cleanQTY(txt: str):
  try:
    string = re.sub(',', '', txt)
    if not(re.search(".",txt)):
      return int(string) 
  
    return float(string) 
  except:
    return None
  