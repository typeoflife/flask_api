import requests

HOST = 'http://127.0.0.1:8080/'
#
# response = requests.post(HOST + 'user',
#                          json={'username': '2b123z4567161', 'email': 'b1zzzzb2345b@mail.ru', 'password': 'b1132DB1231adwa22B1'})
#
# print(response.status_code)
# print(response.json())

#
# response = requests.get(HOST + f'user/{2}')
# print(response)
# print(response.status_code)
# print(response.text)
#
# response = requests.post(HOST + 'adv',
#                          json={'title': 'onetwofree1231sdb', 'text': 'bb15135123@yandex.ru', 'user_id': 2})
# print(HOST + 'adv')
# print(response.status_code)
# print(response.json())

response = requests.delete(HOST + f'adv/{2}')
print(HOST + 'adv')
print(response.status_code)
print(response.json())