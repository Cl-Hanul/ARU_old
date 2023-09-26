import requests as req
from datetime import datetime
from json import load

with open("V2\\API\\key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_key = readFile["gi-sang"]["dan-gi"]["key"]

class dictData:
    class _Body:
        def __init__(self, date:str,items:list) -> None:
            self.date = date
            self.items = items

    def __init__(self, resCode:int = -1,body:None|_Body = None,length = 0) -> None:
        self.resCode = resCode
        self.body = body
        self.length = length

def getWeather(x,y) -> dict:
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
    params ={'serviceKey' : client_key, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : f'{datetime.strftime(datetime.now(),"%Y%m%d")}', 'base_time' : '0600', 'nx' : f"{x}", 'ny' : f"{y}" }

    response = req.get(url, params=params)
    return response.content

if __name__ == "__main__":
    print(getWeather(55,100))