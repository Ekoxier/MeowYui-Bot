from nonebot import on_command, CommandSession
from aiocqhttp import MessageSegment


@on_command('在？', aliases='在?')
async def ping(session: CommandSession):
    msg = MessageSegment.image('https://i0.hdslb.com/bfs/album/d9834281944b168a4b95c26bb7ae47c48cf8910d.jpg') + "buzai"
    await session.send(msg)
