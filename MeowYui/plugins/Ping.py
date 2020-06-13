from nonebot import on_command, CommandSession


@on_command('在？', aliases='在?')
async def ping(session: CommandSession):
    msg = "buzai"
    await session.send(msg)
