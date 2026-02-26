def test_put_v1_account_password (account_helper,prepare_user, generate_random_password, get_activation_token_by_login):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_password = generate_random_password
    token = get_activation_token_by_login

    account_helper.register_new_user(login=login,password=password,email=email)
    account_helper.user_login(login=login, password=password)
    response = account_helper.change_password(login=login, email=email, old_password=password, token=token, new_password=new_password)
    print(response.resource)
    account_helper.user_login(login=login, password=new_password)




