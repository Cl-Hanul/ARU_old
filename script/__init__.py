import random as rd

class AruScript:
    '''
    아르 스크립트입니다.
    
    ---
    
    `문자열`을 넣으면 `리스트`로 바뀌며,
    `리스트`를 넣어주면 랜덤으로 `문자열`이 반환됩니다.
    '''
    def __init__(self,scripts:str|list) -> str:
        if type(scripts) == str:
            self.scripts = [scripts]
        else:
            self.scripts = scripts
    
    def __repr__(self) -> str:
        return rd.choice(self.scripts)

if __name__ == "__main__":
    script = AruScript(['a','b','c'])
    
    print(script)