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
