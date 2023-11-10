# 모듈을 불러옵니다
import os
from json import dump

#######################################


# 모듈 설치
os.system('pip install -r requirements.txt')

#데이터 베이스 추가
for filedata in [["item","{}"],['neis','{"meal":{},"school":{}}'],['twitch',"{}"],['visit',"{}"],['weather','{"positions": {}}'],['artto','{}']]:
    try:
        with open("data\\"+filedata[0]+".json","x",encoding="UTF8") as file:
            file.write(filedata[1])
    except FileExistsError:
        print(f"{filedata[0]}.json 확인 됨. 변경 취소")

print("\n")
# 키 파일 추가
print(os.path.abspath('key.json'))
try:
    with open("key.json","x+") as file:
        key = {"discord":{},
               "naver":{},
               "korean":{},
               "twitch":{},
               "neis":{},
               "weather":{}
        }
        key["discord"]["bot"] = {"token":""}
        key["naver"]["api"] = {"id":"","secret":""}
        key["korean"]["dictionary"] = {"key":""}
        key["twitch"]["api"] = {"id":"","secret":""}
        key["neis"]["api"] = {"secret":""}
        key['weather']['cho-dan-gi'] = {"key":""}
        
        dump(key,file,indent="\t")
except:
    print("\n키 파일이 확인되었습니다.\n만일 키를 작성하지 않은 경우 'key.json'에서 작성해 주세요\n")

os.system("pause")
