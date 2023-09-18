import requests
from json import load
from bs4 import BeautifulSoup

with open("key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_secret = readFile["neis"]["api"]["key"]

class dictData:
    class _Body:
        def __init__(self, school_name,meal_name,meal_date,dishes,calories,ntr) -> None:
            self.school_name = school_name
            self.meal_name = meal_name
            self.meal_date = meal_date
            self.dishes = dishes
            self.calories = calories
            self.ntr = ntr

    def __init__(self, resCode:int = -1,body:list[_Body]|None = None,length = 0) -> None:
        self.resCode = resCode
        self.body = body
        self.length = length

def get_school_by_name(school_name):
    params = {
        "key": client_secret,
        "type": 'json',
        "pindex": 1,
        
        "SCHUL_NM":school_name
    }
    
    resjson = requests.get("https://open.neis.go.kr/hub/schoolInfo",params).json()
    try:
        resjson['schoolInfo']
    except KeyError:
        return None
    else:
        return [{"ofcdc_code":resschool["ATPT_OFCDC_SC_CODE"],"code":resschool["SD_SCHUL_CODE"],"name":resschool["SCHUL_NM"],"pos":f"{resschool['ORG_RDNMA']} ({resschool['ORG_RDNZC']})","code_all":f'{resschool["ATPT_OFCDC_SC_CODE"]}{resschool["SD_SCHUL_CODE"]}'} for resschool in resjson['schoolInfo'][1]['row']]

def get_meal(ofcdc_code,school_code,date):
    params = {
        "key": client_secret,
        "type": 'json',
        "pindex": 1,
        
        "ATPT_OFCDC_SC_CODE": ofcdc_code,
        "SD_SCHUL_CODE": school_code,
        "MLSV_YMD": date,
        
    }

    resjson = requests.get("http://open.neis.go.kr/hub/mealServiceDietInfo",params).json()
    try:
        resjson['mealServiceDietInfo']
    except KeyError:
        return dictData(resjson["RESULT"]["CODE"])
    else:
        reshead:list = resjson['mealServiceDietInfo'][0]['head']
        resdish:list = resjson['mealServiceDietInfo'][1]['row']
        return dictData(reshead[1]["RESULT"]["CODE"],[dictData._Body(dish['SCHUL_NM'], dish['MMEAL_SC_NM'], dish['MLSV_YMD'], dish['DDISH_NM'].replace("<br/>","\n"), dish['CAL_INFO'], dish['NTR_INFO'].split("<br/>")) for dish in resdish],reshead[0]['list_total_count'])

# print(get_school_by_name(""))

# res = get_meal("R10","8981025",20230829)
# if res.resCode == "INFO-000":
#     meals = [meal for meal in res.body]
#     for meal in meals:
#         print("----")
#         print(meal.school_name)
#         print("----")
#         print(meal.meal_date)
#         print(meal.meal_name)
#         print("----")
#         print(meal.dishes)
#         print("----")
#         print(meal.calories)
#         print("----")
#         print(meal.ntr)
#         print("----\n")
# else:
#     print('error')