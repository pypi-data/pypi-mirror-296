from smm_vk.cli.default import cli_group
from smm_vk.cli.groups import subscribers
from smm_vk.cli.object import get_id


@cli_group.group()
def groups():
    pass


groups.add_command(subscribers)


@cli_group.group()
def object():
    pass


object.add_command(get_id)


def main():
    cli_group(_anyio_backend="asyncio")


if __name__ == '__main__':
    main()
