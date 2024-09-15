from smm_vk.utils.base_file_saver import BaseFileSaver


class IdsFileSaver(BaseFileSaver):

    async def save(self, filename: str, values: list[int]) -> None:
        values = "\n".join(map(str, values))
        await self._save_str(filename, values)