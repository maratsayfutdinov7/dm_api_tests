import pprint

import requests

from json import loads

# Почему тесты пишут в функциях def - функции обеспечивают независимость тестов, что упрощает отладку, управление состоянием и выполнение сценариев
def test_post_v1_account():

# # Регистрация пользователя

# # Тестовые данные
    login = 'breeze29121'
    email = f'{login}@mail.ru'
    password = '123456789'

    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'login':login,
        'email': email,
        'password': password
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)

    # Проверка, для отладки
    assert response.status_code == 201, f'Пользователь не был создан {response.json()}'



    # Получить письма из почтового сервера
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    }

    params = {
        'limit': '50',
    }

    response = requests.get('http://185.185.143.231:5025/api/v2/messages', params=params, headers=headers, verify=False)


    print(response.status_code)

    assert response.status_code == 200, 'Письма не были получены'

    # # Получить активационный токен из ConfirmationLinkUrl используя login
    for item in response.json()['items']:
        user_data = loads(item['Content']['Body'])
        user_login = user_data['Login']
        if user_login == login:
            print(user_login)
            token = user_data['ConfirmationLinkUrl'].split('/')[-1]
            print(token)
    assert token is not None, f'Токен для пользователя {login} не был получен'



    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put(f'http://185.185.143.231:5051/v1/account/{token}')
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, 'Пользователь не был активирован'

    # Авторизоваться
    headers = {
        'accept': 'text/plain',
        'Content-Type': 'application/json',
    }
    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)

    assert response.status_code == 200, 'Пользователь не смог авторизоваться'