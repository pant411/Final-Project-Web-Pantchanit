from pythainlp.tokenize import sent_tokenize
from pythainlp.util import countthai
from typing import Tuple
import re
import Utils as ut

def findShopName(lsttext: list, threshold: float = 0.75) -> str:
  listShopName = []
  prefixOrg = ['บริษัท', 'ห้างหุ้นส่วนจำกัด', 'โรงเรียน', 'มหาวิทยาลัย', 'วิทยาลัย', \
   'สำนักงาน', 'ร้าน', 'สหกรณ์', 'วิสาหกิจชุมชน', 'สถาบัน', 'จุฬาลงกรณ์มหาวิทยาลัย', 'ศูนย์']
  suffixOrg = ['จำกัด', '(มหาชน)']
  len_lsttext = len(lsttext)
  for idx in range(len_lsttext):
    res_line = ''
    token_txt = sent_tokenize(lsttext[idx]['txt'], engine='whitespace')
    state = prefixOrg
    keep_able = False
    for ele in token_txt:
      max_res_sim, _ = ut.similarityListWord(ele,state)
      if max_res_sim < threshold and not(keep_able): 
        continue
      elif max_res_sim > threshold and not(keep_able): 
        res_line = res_line + ele + ' '
        keep_able = True
        state = suffixOrg
      elif max_res_sim < threshold and keep_able:
        res_line = res_line + ele + ' '
      elif max_res_sim > threshold and keep_able:
        res_line = res_line + ele
        keep_able = False
        break
      # return ut.spellingCorrecting(res)
      if 'ใบเสร็จรับเงิน' in res_line or 'สำนักงานใหญ่' in res_line: continue
    if len(res_line) > 8:
      listShopName.append(res_line)
  return listShopName 

def findPhoneShop(lsttext: list,listShopTaxID: list) -> str:
  listShopPhone = []
  len_lsttext = len(lsttext)
  for idx in range(len_lsttext):
    pattern = r'\(0\d\)[-\s]?\d{3,4}[-\s]?\d{3,4}|0\d\d?[-\s]?\d{3,4}[-\s]?\d{3,4}-?\d?\d?|\+?66\d?\d?[-\s]?\d{3,4}[-\s]?\d{3,4}-?\d?\d?|0[-/s]?\d\d{2,3}[-/s]?\d{3,4}' 
    list_phone_num = ut.regexFindAll(s = lsttext[idx]['txt'], pattern = pattern)
    # print(list_phone_num)
    phone_num = ''
    for idx in range(len(list_phone_num)):
      phone_num += list_phone_num[idx]
      if idx != len(list_phone_num) - 1:
        phone_num += ','
    if len(phone_num) > 3 and phone_num not in listShopTaxID:
      listShopPhone.append(phone_num)
  return listShopPhone

def findTaxIDShop(lsttext: list, threshold: float = 0.75) -> str:
  listShopTaxID = []
  len_lsttext = len(lsttext)
  for idx in range(len_lsttext):
    taxID = ut.regexSearch(s = lsttext[idx]['txt'], pattern = r"\b\d{13}\b|\b\d{1}[-\s]\d{4}[-\s]\d{5}[-\s]\d{2}[-\s]\d{1}\b|\b\d{3}[-\s]\d{4}[-\s]\d{3}[-\s]\d{3}\b")
    if len(taxID) == 0: 
      res = ''
      keyword = ['เลขประจำตัวผู้เสียภาษี','Tax ID']
      token_txt = sent_tokenize(lsttext[idx]['txt'], engine='whitespace')
      keep_able = False
      for ele in token_txt:
        max_res_sim, _ = ut.similarityListWord(ele,keyword)
        if max_res_sim < threshold and not(keep_able): 
          continue
        elif max_res_sim > threshold and not(keep_able): 
          res = res + ele
          keep_able = True
        elif max_res_sim < threshold and keep_able:
          res = res + ele
        elif max_res_sim > threshold and keep_able:
          keep_able = False
          break      
      taxID = ut.regexSub(s = res, pattern = r"[^0-9-]")
    if len(taxID) >= 13:
      listShopTaxID.append(taxID)
  return listShopTaxID

def findDate(lsttext: list, threshold: float = 0.78):
  listDate = []
  len_lsttext = len(lsttext)
  for idx in range(len_lsttext):
    DateReceipt = ut.regexSearch(s = lsttext[idx]['txt'], pattern = r"\b[0-9]{1,2}[\/.-][0-9]{1,2}[\/.-][0-9]{2,4}\b|\b[0-9]{2,4}[\/.-][0-9]{1,2}[\/.-][0-9]{1,2}\b")
    if len(DateReceipt) == 0 :
      _date = ''
      keyword = ['มกราคม','กุมภาพันธ์','มีนาคม','เมษายน','พฤษภาคม','มิถุนายน','กรกฎาคม','สิงหาคม',\
        'กันยายน','ตุลาคม','พฤศจิกายน','ธันวาคม','ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.',\
        'ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.']
      token_txt = sent_tokenize(lsttext[idx]['txt'], engine='whitespace')
      len_token_txt = len(token_txt)
      for idx in range(len_token_txt):
        max_res_sim, chosen = ut.similarityListWord(token_txt[idx],keyword)  
        # print(max_res_sim, token_txt[idx])  
        if max_res_sim >= threshold and len(token_txt[idx]) >= 2:
          if token_txt[idx-1].isnumeric() and token_txt[idx+1].isnumeric() and\
            int(token_txt[idx-1]) <= 31 and int(token_txt[idx-1]) >= 1 and\
            int(token_txt[idx+1]) >= 1999 and len(token_txt[idx+1]) == 4 and\
            idx < len_token_txt:
              _date = token_txt[idx-1] + ' ' + keyword[chosen] + ' ' + token_txt[idx+1]
          else :
            _date = token_txt[idx]
      if len(_date) > 6:
        listDate.append(_date)
    if len(DateReceipt) > 3:
      listDate.append(DateReceipt)
  return listDate

def findReceiptID(lsttext: list, threshold: float = 0.75) -> str:
  listReceiptID = []
  len_lsttext = len(lsttext)
  for idx in range(len_lsttext):
    res = ''
    keyword = ['เลขที่เอกสาร','เลขที่ / No.']
    token_txt = sent_tokenize(lsttext[idx]['txt'], engine='whitespace')
    keep_able = False
    for ele in token_txt:
      max_res_sim, _ = ut.similarityListWord(ele,keyword)
      # print(max_res_sim, ele)
      if max_res_sim < threshold and not(keep_able): 
        continue
      elif max_res_sim > threshold and not(keep_able): 
        # res = res + ele
        keep_able = True
      elif max_res_sim < threshold and keep_able:
        res = res + ele
      elif max_res_sim > threshold and keep_able:
        keep_able = False
        break      
    if len(res) > 1:
      listReceiptID.append(res)
  return listReceiptID

def findCustomerShop(lsttext: list, line_end: int, threshold: float = 0.75):
  listCustomerShop = []
  len_lsttext = len(lsttext)
  # print(lsttext)
  keep_able = False
  print(line_end)
  for idx in range(len_lsttext):
    res = ''
    keyword = ['sold to','Customer','ลูกค้า','ผู้จ่าย','นามผู้ชื้อ','ผู้ชื้อ','ขายให้','ได้รับเงินจาก','ชื่อ-สกุล']
    end_word = ['วันที่','เลขประจําตัวผู้เสียภาษี','เลขที่เอกสาร','ผู้ติดต่อ','ใบเสร็จรับเงิน','no']
    token_txt = sent_tokenize(lsttext[idx]['txt'], engine='whitespace')
    if not(keep_able): keep_able = False
    # print(token_txt)
    for ele in token_txt:
      max_res_sim, _ = ut.similarityListWord(ele,keyword)
      max_end_sim, _ = ut.similarityListWord(ele,end_word)
      # print(max_res_sim, ele)
      # print(max_end_sim, ele)
      if max_res_sim < threshold and not(keep_able): 
        continue
      elif res != '' and keep_able and max_end_sim > 0.75:
        print("stop")
        keep_able = False
        break      
      elif max_res_sim >= threshold and len(ele) >= 4 and not(keep_able): # เจอ keyword
        # res = res + ele + ' '
        keep_able = True
      elif max_res_sim < threshold and keep_able:
        res = res + ele + ' '
      elif max_res_sim >= threshold and res == ' ' and keep_able:
        # keep_able = False
        continue 

    print(res)
    if len(res) > 4 and countthai(res, ignore_chars="") >= 70 :    
      listCustomerShop.append(res)
        
    if lsttext[idx]['line-num'] == line_end-1: # ห่างจากที่อยู่ของลูกค้าอยู่ 1 บรรทัดหรือไม่
      break      

  return listCustomerShop   

def patternAddress(text: str,start_pt: int = 0):
  keywords = ["buildingNo", "buildingTitle", "floor", "villageNo", "alley",\
    "junction", "street", "subDistrict", "district", "province", "postalCode"] 
  regExKey = [
    "\s?(บ้านเลขที่|เลขที่\.)?[1-9][0-9]{0,2}(\/[1-9][0-9]{0,2})?\s","\s?(อาคาร|ตึก|หมู่บ้าน)\S*",\
    "\s?(ชั้น|ชั้นที่)","\s?(หมู่ที่|หมู่|ม\.)","\s?(ตรอก|ซอย|ซ\.)\S*",\
    "\s?แยก\s[1-9][0-9]{0,2}(\/[1-9][0-9]{0,2})?",\
    "\s?(ถนน|ถ\.)\S*","\s?(ตำบล|ต\.|แขวง)\S*","\s?(อำเภอ|อ\.|เขต)\S*",\
    "\s?(จังหวัด|จ\.|กรุงเทพมหานคร|กทม\.|กรุงเทพฯ)\S*","\s([1-9][0-9]{4})"
  ]
  position_start = 9999999
  position_end = 0
  keyword_start = ''
  keyword_end = ''
  keyword_start_index = 0
  keyword_end_index = 0
  count_key = 0
  for idx in range(start_pt,len(regExKey)):
    search_key = re.search(regExKey[idx], text)
    if search_key:
      # print(idx)
      # print(search_key)
      # print(keywords[idx])
      count_key += 1
      if position_start > search_key.start():
        keyword_start = keywords[idx]
        keyword_start_index = idx
        position_start = search_key.start()
        position_end = search_key.start()  

      if position_end < search_key.end():
        keyword_end = keywords[idx]
        keyword_end_index = idx
        position_end = search_key.end()
  # print(position_start,position_end)
  try: 
    res_txt = text[position_start:position_end+1]
    # print(res_txt)
    if position_start == 0 and position_end == 0: 
      # print("f111")
      return None
    elif position_start == 9999999:
      # print("f222")
      return None
    elif position_end-position_start+1 < 5 or countthai(res_txt, ignore_chars="") <= 20:
      # print("f333")
      return None
    elif count_key < 2 and position_start >= 7:
      # print("f444")
      return None
    elif (count_key/(keyword_end_index-keyword_start_index+1)) > 0.2:
      print(f'total keyword is {count_key}')
      # print(res_txt)
      return {
        "position-start": position_start,
        "keyword-start": keyword_start,
        "keyword-start-index": keyword_start_index,
        "position-end": position_end,
        "keyword-end": keyword_end,
        "keyword-end-index": keyword_end_index,
        "number-keyword": count_key,
        "text": res_txt
      }      
  except IndexError:
    return None

def findListAddress(lsttext: list):
  size_of_pt = 11
  start_pt = 0
  listAddress = []
  len_lsttext = len(lsttext)
  cannot_find = 0
  # prevPosEndKeyword = 0
  for idx in range(len_lsttext):
    patternAddr = patternAddress(lsttext[idx]['txt'],start_pt)
    if patternAddr:
      # print(patternAddr)   
      posStartKeyword = patternAddr["keyword-start-index"]
      posEndKeyword = patternAddr["keyword-end-index"]
      # totalKeyword = patternAddr["total-keyword"]
      addr = patternAddr["text"]
      listAddress.append({
        "keyword-start-index": posStartKeyword,
        "keyword-end-index": posEndKeyword,
        "number-keyword": patternAddr["number-keyword"],
        "line-num": lsttext[idx]['line-num'],
        "address": addr
      })
      if posEndKeyword < size_of_pt-1:
        start_pt = posEndKeyword+1
      else:
        start_pt = 0
      # print(posStartKeyword, posEndKeyword)
      # print(addr)
    else:
      cannot_find += 1
      if cannot_find == 2: 
        start_pt = 0
        cannot_find = 0

  return listAddress

def extractAddress(lsttext: list, line_item_txt1_p1: Tuple[int,int],\
    line_item_txt1_p2: Tuple[int,int]):
  listAddress = findListAddress(lsttext)
  # print(listAddress)
  addr_1 = ""
  line_addr_1 = 0
  addr_2 = ""
  line_addr_2 = 0
  # prev_start = 0 
  prev_end = 0 
  state = 0 # 0 = addr_1 , 1 = addr_2
  # print(line_item_txt1_p1)
  # print(line_item_txt1_p2)
  # range_p1 = range(line_item_txt1_p1[0],line_item_txt1_p1[1]+1)
  range_p2 = range(line_item_txt1_p2[0],line_item_txt1_p2[1]+1)
  for ele in listAddress:
    if (state == 0 and ele["keyword-start-index"] < 3 and prev_end >= 9) or (ele["line-num"] in range_p2):
      state = 1
      if addr_2 == "" and line_addr_2 == 0: 
        line_addr_2 = ele["line-num"]
      addr_2 = addr_2 + ele["address"]
      # prev_start = ele["keyword-start-index"]
    elif (state == 0 and addr_1 == "") or (ele["keyword-end-index"] <= 10 and state == 0) :
      if addr_1 == "" and line_addr_1 == 0: 
        line_addr_1 = ele["line-num"]
      addr_1 = addr_1 + ele["address"]
      # line_addr_1 = ele["line-num"]
      # prev_start = ele["keyword-start-index"]
      prev_end = ele["keyword-end-index"]
      if ele["keyword-end-index"] == 10:
        state = 1
    elif ele["keyword-start-index"] >= 8 and addr_2 == "" and state == 1:
      continue
    elif ele["keyword-end-index"] <= 10 and state == 1:
      if addr_2 == "" and line_addr_2 == 0: 
        line_addr_2 = ele["line-num"]
      addr_2 = addr_2 + ele["address"]
      # line_addr_2 = ele["line-num"]
      # prev_start = ele["keyword-start-index"]
      prev_end = ele["keyword-end-index"] 
    # print("===========")
    # print(line_addr_1)       
    # print(line_addr_2)
    # print("===========")
    # print(state)

  if line_addr_2 in range_p2: # กรณีที่ที่อยู่ของร้านค้าอยู่ด้านล่างสุดของใบเสร็จ
    return {
      "addr-shop": addr_2,
      "line-addr-shop": line_addr_2,
      "addr-customer": addr_1,
      "line-addr-customer": line_addr_1
    }
  return {
      "addr-shop": addr_1,
      "line-addr-shop": line_addr_1,
      "addr-customer": addr_2,
      "line-addr-customer": line_addr_2
  }

def findListOfItem(lsttext: list, threshold: float = 0.75):
  keywords = ["รายการ", "ลำดับที่", "รายการสินค้า", "รายการที่ชำระ", "ชื่อสินค้า", "รายละเอียด"]
  listAddressItem = []
  len_lsttext = len(lsttext)
  keep_able = False
  for idx in range(len_lsttext):
    token_txt = sent_tokenize(lsttext[idx]['txt'], engine='whitespace')
    if not(keep_able):
      for ele in token_txt:
        max_res_sim, _ = ut.similarityListWord(ele,keywords)
        if max_res_sim >= threshold and not(keep_able):
          listAddressItem.append(lsttext[idx]['txt'])
          keep_able = True
          break
    else:
      listAddressItem.append(lsttext[idx]['txt'])
  return listAddressItem 
