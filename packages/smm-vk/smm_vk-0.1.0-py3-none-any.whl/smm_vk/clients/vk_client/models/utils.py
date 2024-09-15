from enum import Enum

from pydantic import BaseModel


class EntityType(str, Enum):
    user = "user"
    group = "group"
    event = "event"
    page = "page"
    application = "application"
    vk_app = "vk_app"


class EntityByScreenName(BaseModel):
    object_id: int
    type: EntityType
