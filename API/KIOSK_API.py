#pip install bson -t MyLayer\python
# 날씨 스크래핑 모듈
import API.weather_recommendation as weather_recommendation 

# 현재 AWS API 서버에서 실행 중인 코드.
def getExtractedMenu(txt, _list):
  recommennd = weather_recommendation.scrape_wether() #웹스크래핑
  
  mylist = []
  for item in _list:
    if(txt.find(item)>=0):
      mylist.append(item)
  return mylist

# """텍스트에 리스트의 아이템이 들어있는지 확인하는 메소드"""
# def getExtractedMenubyAPI(txt, _list):
#   API_URL = '이 URL 을 교체해서 실행'
#   param = {'mylist':_list, 'sentence':txt}
#   return requests.get(url=API_URL,params=param).json()