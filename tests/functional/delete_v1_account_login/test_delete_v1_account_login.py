def test_delete_v1_account_login(auth_account_helper):
    response = auth_account_helper.logout_client()
    return response