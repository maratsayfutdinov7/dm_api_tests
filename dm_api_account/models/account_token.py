from pydantic import BaseModel, Field, ConfigDict

class AccountToken(BaseModel):
    model_config = ConfigDict(extra='forbid')
    token: str = Field(..., description="Токен активации пользователя")