from nonebot import on_command, CommandSession, on_natural_language
from aiocqhttp import MessageSegment


@on_natural_language(keywords={'我好了'}, only_to_me=False)
async def ping(session: CommandSession):
    msg = "不许好"
    await session.send(msg)