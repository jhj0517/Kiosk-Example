from deep_translator import GoogleTranslator
import nltk
from nltk.tokenize import word_tokenize
from word2number import w2n
from API.konrum import convert as n2k

#최초 실행시 실행시켜야 되는 메소드
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

"""문장에서 리스트의 변수들을 뽑아내는 메소드"""
def getWordsFromList(_txt,_list):
  mylist = []
  for item in _list:
    if(_txt.find(item)>=0):
      mylist.append(item)
  return mylist

"""NLP로 문장에서 숫자를 뽑아내는 메소드"""
def extract_nums(txt):
    translated = GoogleTranslator(source='auto', target='en').translate(txt)  
    tokens = word_tokenize(translated)
    poses = nltk.pos_tag(tokens)

    numlist = []
    for p in poses:
        if(p[1]=='CD'):
            numlist.append(p[0])
        #'one'이 아니라 'a' 로 번역할 때
        elif(p[1]=='DT' and p[0]=='a'):
            numlist.append("one")

    for i in range(len(numlist)):
        numlist[i] = w2n.word_to_num(numlist[i])
    return numlist


"""뽑아낸 숫자 리스트와 메뉴 리스트를 서로 합침"""
def grouping_withMenuAndNums(_menu,_nums):
    groupingList =[]
    if(len(_menu)==len(_nums)):
        for i in range(len(_menu)):
            groupingList.append((_menu[i] ,_nums[i]))
    return groupingList        

"""합친 리스트로 문장을 만들어내는 메소드""" 
def makeTextwithMenuAndNum(_menu,_nums):
    _list = grouping_withMenuAndNums(_menu,_nums)
    first = "주문하신 메뉴는" 
    middle = ""           
    for item in _list:
        print(item[1])
        num = n2k(item[1], 수사='양수사-관형사', 한자어=False)
        middle += f' {item[0]} {num} 개,'
    end = "으로 확인 되었습니다."
    return first + middle + end   