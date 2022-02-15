import requests

HOST = 'http://127.0.0.1:8080/'
#
# response = requests.post(HOST + 'user',
#                          json={'username': '123z4567161', 'email': '1zzzb2345b@mail.ru', 'password': 'b1132DB1231adwa22B1'})
#
# print(response.status_code)
# print(response.json())


# response = requests.get(HOST + f'user/{9}')
# print(response)
# print(response.status_code)
# print(response.text)
#
response = requests.post(HOST + 'adv',
                         json={'title': 'imbalance1231sdb', 'text': 'imba15135123@yandex.ru', 'user_id': 8})
print(HOST + 'adv')
print(response.status_code)
print(response.json())

# response = requests.delete(HOST + f'adv/{9}')
# print(HOST + 'adv')
# print(response.status_code)
# print(response.json())