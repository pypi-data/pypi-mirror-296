import typing as t
from abc import ABC, abstractmethod

import aiofiles


class BaseFileSaver(ABC):

    @abstractmethod
    async def save(self, filename: str, values: t.Any) -> None:
        ...

    @staticmethod
    async def _save_str(filename: str, values: str) -> None:
        async with aiofiles.open(filename, mode='w') as f:
            await f.write(values)