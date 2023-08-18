import requests
from json import load


with open("API\\key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_id = readFile["naver"]["dictionary"]["id"]
    client_secret = readFile["naver"]["dictionary"]["secret"]

class dictData:
    class _Body:
        def __init__(self, date:str,items:list) -> None:
            self.date = date
            self.items = items

    def __init__(self, resCode:int = -1,body:None|_Body = None,length = 0) -> None:
        self.resCode = resCode
        self.body = body
        self.length = length

def searchWordOnDictionary(word:str):

    encText = word
    limitNumber = "3"

    url = f"https://openapi.naver.com/v1/search/encyc.json?query={encText}&display={limitNumber}"
    headers = {
        "X-Naver-Client-Id":client_id,
        "X-Naver-Client-Secret":client_secret
    }

    response:requests.Response = requests.get(url,headers=headers)
    resCode = response.status_code

    if(resCode==200):
        resContent = response.json()
        return dictData(resCode,dictData._Body(resContent["lastBuildDate"],resContent["items"]),resContent["display"])
    else:
        return dictData(resCode,None)

if __name__ == "__main__":
    gw = searchWordOnDictionary("돌") #예: '돌'
    for i in gw.body.items:
        print(i["title"])
        print(i["description"])
        print("\n\n")
    print(gw.body.date)