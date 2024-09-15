from urllib.parse import urlparse

from aiovk import TokenSession, API, ImplicitSession

from smm_vk.clients.vk_client.models.groups import Group
from smm_vk.clients.vk_client.models.utils import EntityByScreenName


class VkClientV1:

    def __init__(self, session: TokenSession | ImplicitSession) -> None:
        self._client = API(session)

    async def get_group(self, group_id: int) -> Group:
        result = await self._client.groups.getById(group_id=group_id, fields='members_count')
        return Group.model_validate(result[0])

    async def get_group_members(
        self,
        group_id: int,
        filters: str = "",
        offset: int = 0,
        limit: int = 1000
    ) -> list[int]:
        result = await self._client.groups.getMembers(group_id=group_id, offset=offset, count=limit, filter=filters)
        return result['items']

    async def get_group_subscribers(self, group_id: int, unsure: bool = False) -> list[int]:
        count = (await self.get_group(group_id)).members_count
        members = []
        for i in range(0, count, 1000):
            members += await self.get_group_members(group_id=group_id, offset=i)

        if not unsure:
            return members

        unsure_members = []
        for i in range(0, count, 1000):
            unsure_members = await self.get_group_members(group_id=group_id, offset=i, filters='unsure')
        return members + unsure_members

    async def get_id_by_url(self, url: str) -> EntityByScreenName:
        parsed_url = urlparse(url)
        screen_name = parsed_url.path.split('/')[-1]
        result = await self._client.utils.resolveScreenName(screen_name=screen_name)
        return EntityByScreenName.model_validate(result)
