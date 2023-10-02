import requests as req
from datetime import datetime as dt
from json import load,loads, dumps
import xmltodict as xml

with open("key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_key = readFile["kor-law"]["api"]["OC"]

class dictData:
    def __init__(self, resCode:int = -1,items:list = []) -> None:
        self.resCode = resCode
        self.items = items

def SearchLaw(searchtype:int,q:str) -> list[dict]|None:
    '''
    ### searchtype
    1 | 법령명 검색\n
    2 | 법령 내용검색
    
    ---
    '''
    url = 'http://www.law.go.kr/DRF/lawSearch.do?target=law'
    params = {
        "OC":client_key,
        "type":"xml",
        "search":searchtype,
        "query":q
    }
    response = req.get(url, params=params)
    result = loads(dumps(xml.parse(response.content)))['LawSearch']
    if result['totalCnt'] == '0':
        return None
    return result['law']
    

if __name__ == "__main__":
    now = dt.now()
    print(SearchLaw(1,"자동차"))