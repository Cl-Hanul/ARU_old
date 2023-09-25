# import csv
# import json
# from pandas import read_csv
# import requests as req
# from io import StringIO

# res = req.get("https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm=202211300900&stn=0&help=1&authKey=pgyq-jnNQgmMqvo5zVIJzQ")

# with StringIO(str(res.content,'ansi')) as file:
#     data = json.dumps(list(csv.DictReader(file)))
#     print(data)
######################################
# import requests
# import json

# # URL 문자열
# url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?tm=202211300900&stn=0&help=1&authKey=pgyq-jnNQgmMqvo5zVIJzQ'

# # GET 요청
# response = requests.get(url)

# # 응답을 JSON 형태로 변환
# json_response = response.json()

# print(json_response)
##########################################
# data = []
# with open('data.csv', 'r') as csv_file:
#     reader = csv.DictReader(csv_file)
#     data = list(reader)

# json_data = json.dumps(data)
# print(json_data)