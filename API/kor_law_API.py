import requests as req
from datetime import datetime as dt
from json import load

with open("key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_key = readFile["weather"]["cho-dan-gi"]["key"]

class dictData:
    def __init__(self, resCode:int = -1,items:list = []) -> None:
        self.resCode = resCode
        self.items = items

def SearchLaw() -> dictData|None:
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    params = {}
    response = req.get(url, params=params)

if __name__ == "__main__":
    now = dt.now()
    print(SearchLaw())