import requests
from bs4 import BeautifulSoup
import re

def scrape_wether(): 
    url="https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD+%EB%82%A0%EC%94%A8&oquery=%EB%82%A0%EC%94%A8&tqi=hpLfIdprvhGss4ey9pNssssstTs-425794"
    session = requests.Session()
    head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}
    res = session.get(url=url,headers=head).content
    soup =BeautifulSoup(res,"html.parser")
    temperature=soup.find("div",attrs={'class':"dsc"})
    temper= temperature.find("span",attrs={'class':'scal temp'}).text
    weather = temperature.get("title")
    return [weather,temper]

def get_recommendedList():
    datas = scrape_wether()
    weather = datas[0] 
    ntemper = float(datas[1])
    
    if(weather == "맑음"):
        if( ntemper>32):
            recommended = ['물냉면','비빔냉면','삼계탕', '메밀소바']
        elif(ntemper< 5):
            recommended = ['라면','만두국','갈비탕','순두부찌개']
        else:
            recommended = ['오징어덮밥','제육덮밥','돈까스덮밥','김치볶음밥','낙지볶음밥','오므라이스','불고기덮밥','햄버거','라면','만두국','갈비탕','순두부찌개','물냉면','비빔냉면','삼계탕', '메밀소바','떡볶이']

    elif(weather == "비"):
        if(ntemper>32):
            recommended = ['물냉면','비빔냉면','삼계탕', '메밀소바']
        elif(ntemper< 5):
            recommended = ['라면','만두국','갈비탕','순두부찌개']
        else:
            recommended = ['오징어덮밥','제육덮밥','돈까스덮밥','김치볶음밥','낙지볶음밥','오므라이스','불고기덮밥','햄버거','라면','만두국','갈비탕','순두부찌개','물냉면','비빔냉면','삼계탕', '메밀소바','떡볶이']
    
    else:
        if(ntemper>32):
            recommended = ['물냉면','비빔냉면','삼계탕', '메밀소바']
        elif(ntemper< 5):
            recommended = ['라면','만두국','갈비탕','순두부찌개']
        else:
            recommended = ['오징어덮밥','제육덮밥','돈까스덮밥','김치볶음밥','낙지볶음밥','오므라이스','불고기덮밥','햄버거','라면','만두국','갈비탕','순두부찌개','물냉면','비빔냉면','삼계탕', '메밀소바','떡볶이']
    
    return recommended
