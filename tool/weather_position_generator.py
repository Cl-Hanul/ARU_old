from openpyxl import load_workbook
from json import dump

kor_positions = load_workbook("tool/kor_position(20230611).xlsx", data_only=True)['최종 업데이트 파일_20230611']

def REALNone(string):
    if string == None:
        return ''
    else:
        return string
# data = {
#     "position":[f"{REALNone(row1[0].value)} {REALNone(row2[0].value)} {REALNone(row3[0].value)}" for row1,row2,row3 in zip(kor_positions['C2':'C3796'],kor_positions['D2':'D3796'],kor_positions['E2':'E3796'])],
#     "coord":[{"x":x[0].value,"y":y[0].value} for x,y in zip(kor_positions['F2':'F3796'],kor_positions['G2':'G3796'])]
# }
data = {}
now = ''
for i in range(2,3797):
    row = kor_positions[f'C{i}']
    if row.value != now:
        now = row.value
        data[now] = []

    data[now].append({
        "name":f"{kor_positions[f'C{i}'].value} {kor_positions[f'D{i}'].value} {kor_positions[f'E{i}'].value}",
        "coord":{"x":kor_positions[f'F{i}'].value,"y":kor_positions[f'G{i}'].value}
    })

with open("info\\kor_position.json","wt") as file:
    dump(data,file,indent="\t")