# 모듈을 불러옵니다
import os
from json import dump

#######################################


# 모듈 설치
os.system('pip install -r requirements.txt')

# 키 파일 추가
print(os.path.abspath('key.json'))
try:
    with open("key.json","x+") as file:
        key = {"discord":{},
               "naver":{},
               "korean":{},
               "twitch":{}}
        key["discord"]["bot"] = {"token":""}
        key["naver"]["api"] = {"id":"","secret":""}
        key["korean"]["dictionary"] = {"key":""}
        key["twitch"]["api"] = {"id":"","secret":""}
        
        dump(key,file,indent="\t")
except:
    print("\n키 파일이 확인되었습니다.\n만일 키를 작성하지 않은 경우 'key.json'에서 작성해 주세요\n")