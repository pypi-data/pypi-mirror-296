from pydantic import BaseModel


class Group(BaseModel):
    id: int
    members_count: int | None = None
    name: str
    screen_name: str
    is_closed: int
    type: str
    is_admin: int
    admin_level: int | None = None
    is_member: int
    is_advertiser: int
    photo_50: str | None = None
    photo_100: str | None = None
    photo_200: str | None = None
