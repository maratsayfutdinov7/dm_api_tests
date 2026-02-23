from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)

# ... - обязательное поле, ConfigDict(extra='forbid') - обязательное для заполнение поле (!= null)
class LoginCredentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    login: str = Field(..., description='Логин')
    password: str = Field(..., description='Пароль')
    remember_me: bool = Field(..., description='Запомнить меня', serialization_alias='rememberMe')