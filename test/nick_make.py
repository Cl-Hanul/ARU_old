from typing import Literal
from random import choice

JAUM = {
    "1":['ㄱ','ㄷ','ㅂ','ㅅ','ㅈ'],
    "2":['ㄲ','ㄸ','ㅃ','ㅆ','ㅉ'],
    "3":['ㅋ','ㅌ','ㅍ','ㅊ'],
    "4":['ㄴ','ㅁ','ㅇ','ㄹ']
}

MOUM_DAN = {
    "1":['ㅏ','ㅐ','ㅗ','ㅚ'],
    "2":['ㅓ','ㅔ','ㅜ','ㅟ','ㅡ']
}
MOUM_IJOONG = {
    "1":['ㅑ','ㅒ','ㅘ','ㅛ'],
    "2":['ㅕ','ㅖ','ㅞ','ㅠ','ㅢ']
}

JOONG = "ㅣ"

def make_nick(repeat:int,jaumType:Literal['1','2','3','4'],moumType:Literal['1','2'],DanI:Literal["Danmoum","IjoongMoum"],useJoongseoung:bool,batchim:bool) -> str:
    '''
    ### jaumType `자음 타입`
    - 1. 순하고 부드러움
    - 2. 강하고 단단함
    - 3. 크고 거셈
    - 4. 울림
    
    ### moumType `모음 타입`
    - 1. 양성 모음 조화
    - 2. 음성 모음 조화
    
    ### DanI `단모음 or 이중모음`
    ### useJoongseoung `중성모음 사용 여부`
    
    '''
    jaums = JAUM[jaumType]
    if DanI == "Danmoum":
        moums = MOUM_DAN[moumType]
    else:
        moums = MOUM_IJOONG[moumType]
    if useJoongseoung:
        moums.append(JOONG)
    
    returns = []
    for i in range(repeat):
        returns.append([choice(jaums),choice(moums)])
        if batchim:
            returns[-1].append(choice(jaums))
        
    
    return returns

if __name__ == "__main__":
    print(make_nick(2,'1','1','IjoongMoum',True,True))