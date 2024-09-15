import asyncio

from aiovk import TokenSession

from smm_vk.clients.vk_client.driver import DefaultDriver
from smm_vk.configs import config
from smm_vk.containers.vk_client import VkClientContainer
from smm_vk.utils.singleton import Singleton


class ApplicationDI:
    __metaclass__ = Singleton

    def __init__(self):
        session = TokenSession(config.vk_auth.TOKEN, driver=DefaultDriver(loop=asyncio.get_event_loop()))
        self.vk_client_container = VkClientContainer(session)


DI = ApplicationDI()
