from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

# ... - обязательное поле, ConfigDict(extra='forbid') - обязательное для заполнение поле (!= null)
class ChangePassword(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    token: str = Field(description='Токен')
    old_password: str = Field(..., description='Пароль',serialization_alias='oldPassword')
    new_password: str = Field(..., description='Пароль',serialization_alias='newPassword')
