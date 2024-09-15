import asyncclick as click
from aiovk import TokenSession

from smm_vk.clients.vk_client.driver import DefaultDriver
from smm_vk.clients.vk_client.vk_client import VkClientV1
from smm_vk.configs import config
from smm_vk.utils.ids_file_saver import IdsFileSaver


@click.command()
@click.option('--url', prompt="Ссылка на группу", type=str, help="Cсылка на группу")
@click.option('--file', required=False, type=str, help="Имя файла")
@click.option('--unsure', required=False, type=bool, help="Возможно, пойду (ивенты)")
async def subscribers(url: str, file: str) -> None:
    session = TokenSession(config.vk_auth.TOKEN, driver=DefaultDriver())
    client = VkClientV1(session)
    event = await client.get_id_by_url(url)
    data = await client.get_group_subscribers(event.object_id)
    if file:
        await IdsFileSaver().save(f"{file}.txt", data)
    else:
        click.echo(" \n".join(map(str, data)))
    await session.close()
