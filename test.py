import requests
from xml.etree import ElementTree

url = "http://api.visitkorea.or.kr/openapi/service"
key = "G3F+WRzH8kILU688dICDELAp76JX6NIHf+Um+ZrXtfqndx9EunGlsOGQ9pNtIu64iHIYpIq7670C1VUd84kKPw=="

param ={
    "ServiceKey":key,
    "numOfRows":10,
    "pageNo":1,
    "MobileOS":"WIN",
    "MobileApp":"AppTest",
    "arrange":"A",
    "listYN":"Y",
    "eventStartDate":20170901
}
response = requests.get(url=url,params=param).content
#print(response.decode('utf-8'))


tree = ElementTree.fromstring(response.decode('utf-8'))

print(tree)