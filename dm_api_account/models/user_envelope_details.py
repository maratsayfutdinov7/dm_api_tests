from datetime import datetime
from typing import (
    Optional,
    Any,
    List,
)

from pydantic import (
    BaseModel,
    ConfigDict,
)


class Rating(BaseModel):
    enabled: bool
    quality: int
    quantity: int


class Info(BaseModel):
    value: str
    parseMode: str


class Paging(BaseModel):
    postsPerPage: int
    commentsPerPage: int
    topicsPerPage: int
    messagesPerPage: int
    entitiesPerPage: int


class Settings(BaseModel):
    colorSchema: str
    nannyGreetingsMessage: Optional[str] = None
    paging: Paging


class Resource(BaseModel):
    login: str
    roles: List[str]
    online: str
    registration: datetime
    rating: Rating
    settings: Settings
    mediumPictureUrl: Optional[str] = None
    smallPictureUrl: Optional[str] = None
    status: Optional[str] = None
    name: Optional[str] = None
    location: Optional[str] = None
    icq: Optional[str] = None
    skype: Optional[str] = None
    originalPictureUrl: Optional[str] = None
    info: Optional[Any] = None


class UserEnvelopeDetails(BaseModel):
    model_config = ConfigDict(extra='forbid')
    resource: Resource
    metadata: Optional[Any] = None