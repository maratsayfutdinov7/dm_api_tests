import pprint

import requests

# curl -X 'POST' \
#   'http://185.185.143.231:5051/v1/account' \
#   -H 'accept: */*' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "login": "string",
#   "email": "string",
#   "password": "string"
# }'

# url = 'http://185.185.143.231:5051/v1/account'
# headers = {
#        'accept': '*/*',
#        'Content-Type': 'application/json'
# }
# json = {
#   "login": "breeze1123",
#   "email": "breeze1123@mail.ru",
#   "password": "breeze1123"
# }
# # requests.post - функция которая вызывает метода post из библиотеки requests в Python, который отправляет HTTP-запрос POST на указанный URL и сохраняет его в response.
#
# response = requests.post(
#     url=url,
#     headers=headers,
#     json=json
# )
# print(response.status_code)



#curl -X 'PUT' \
#  'http://185.185.143.231:5051/v1/account/77f3c894-87a4-4c87-9b3b-d90551d849fd' \
#  -H 'accept: text/plain' \
#  -H 'X-Dm-Auth-Token: 7f3c894-87a4-4c87-9b3b-d90551d849fd' \
#  -H 'X-Dm-Bb-Render-Mode: 7f3c894-87a4-4c87-9b3b-d90551d849fd'



url = 'http://185.185.143.231:5051/v1/account/77f3c894-87a4-4c87-9b3b-d90551d849fd'
headers = {
       'accept': 'text/plain'

}

response = requests.put(
    url=url,
    headers=headers
)
print(response.status_code)
pprint.pprint(response.json())