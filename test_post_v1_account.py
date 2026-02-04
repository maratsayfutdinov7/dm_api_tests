import requests


# Почему тесты пишут в функциях def - функции обеспечивают независимость тестов, что упрощает отладку, управление состоянием и выполнение сценариев
def test_post_v1_account():
    # Регистрация пользователя
    headers = {
        'accept': '*/*',
        'Content-Type': 'application/json',
    }

    json_data = {
        'login': 'string',
        'email': 'string',
        'password': 'string',
    }

    response = requests.post('http://185.185.143.231:5051/v1/account', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)

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
    print(response.text)
    # Получить активационный токен
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    }

    response = requests.get(
        'http://185.185.143.231:5025/api/v1/messages/yFnvZTONvy21qTYfeeiYrYydBffLLHXQDZaaDfa6i4g=@mailhog.example',
        headers=headers,
        verify=False,
    )
    print(response.status_code)
    print(response.text)

    # Активация пользователя
    headers = {
        'accept': 'text/plain',
    }

    response = requests.put('http://185.185.143.231:5051/v1/account/77f3c894-87a4-4c87-9b3b-d90551d849fd')
    print(response.status_code)
    print(response.text)

    # Авторизоваться
    headers = {
        'accept': 'text/plain',
        'Content-Type': 'application/json',
    }
    json_data = {
        'login': 'string',
        'password': 'string',
        'rememberMe': True,
    }

    response = requests.post('http://185.185.143.231:5051/v1/account/login', headers=headers, json=json_data)
    print(response.status_code)
    print(response.text)