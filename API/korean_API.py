import requests as req
from urllib3.exceptions import InsecureRequestWarning
req.packages.urllib3.disable_warnings(InsecureRequestWarning)
from json import load

#https://opendict.korean.go.kr/api/search?certkey_no=5757&key={{KEY}}&target_type=search&req_type=json&part=word&q={{query}}&sort=dict&start=1&num=10

with open("V2\\API\\key.json","r",encoding="utf-8") as file:
    readFile = load(file)
    client_key = readFile["korean"]["dictionary"]["key"]


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

    url = f"https://opendict.korean.go.kr/api/search?certkey_no=5757&key={client_key}&target_type=search&req_type=json&part=word&q={encText}&sort=dict&start=1&num=10"

    response:req.Response = req.get(url,verify=False)
    resCode = response.status_code

    if(resCode==200):
        resContent = response.json()
        return dictData(resCode,dictData._Body(resContent["channel"]["lastbuilddate"],resContent["channel"]["item"]),resContent["channel"]["num"])
    else:
        return dictData(resCode,None)

print(searchWordOnDictionary("a").body.items)