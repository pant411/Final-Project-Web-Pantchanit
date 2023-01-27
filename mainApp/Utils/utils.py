from Levenshtein import jaro
import re
from collections import Counter
# from pythainlp.spell import NorvigSpellChecker
# from pythainlp.tokenize import sent_tokenize
# import sys
# adding Folder_2 to the system path
# from readDictFile import readDictTuple

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
