import asyncclick as click
from aiovk import TokenSession

from smm_vk.clients.vk_client.driver import DefaultDriver
from smm_vk.clients.vk_client.vk_client import VkClientV1
from smm_vk.configs import config


@click.command()
@click.option('--url', prompt="Ссылка на объект", type=str, help="Введите ссылку на объект")
async def get_id(url: str):
    session = TokenSession(config.vk_auth.TOKEN, driver=DefaultDriver())
    client = VkClientV1(session)
    event = await client.get_id_by_url(url)
    click.echo(f"Идентификатор: {event.object_id}, тип: {event.type.value}")
    await session.close()
