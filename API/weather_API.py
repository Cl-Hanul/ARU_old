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

def getWeather(datetime:dt,x,y) -> dictData|None:
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    generated_datetime = datetime.replace(hour=(datetime.hour//3-1)*3+2)
    params = {'serviceKey' : client_key, 'pageNo' : '1', 'numOfRows' : '1000', 'dataType' : 'JSON', 'base_date' : f'{generated_datetime.strftime("%Y%m%d")}', 'base_time' : f'{generated_datetime.strftime("%H")}00', 'nx' : f"{x}", 'ny' : f"{y}" }
    response = req.get(url, params=params)
    response2json = response.json()
    return_data = None
    return_data = dictData(response2json['response']['header']['resultCode'],[])
    if return_data.resCode != '00':
        print(return_data.resCode)
        return None
    for weatherdata in response2json['response']['body']['items']['item']:
        weathertime = '{0}_{1}'.format(weatherdata["fcstDate"],weatherdata["fcstTime"])
        
        if len(return_data.items) == 0:
            return_data.items.append({})
            return_data.items[-1]['WeatherTime'] = weathertime
        
        if  return_data.items[-1]['WeatherTime'] != weathertime:
            return_data.items.append({})
            return_data.items[-1]['WeatherTime'] = weathertime
        
        return_data.items[-1][weatherdata['category']] = weatherdata['fcstValue']
    return return_data

if __name__ == "__main__":
    now = dt.now()
    print(getWeather(now,55,100).items)