from nonebot import on_command, CommandSession, on_natural_language
from aiocqhttp import MessageSegment


@on_natural_language(keywords={'我好了'}, only_to_me=False)
async def wo_hao_le(session: CommandSession):
    msg = "不许好"
    await session.send(msg)


'''
@on_command('我喜欢你')
async def wo_xi_huan_ni(session: CommandSession):
    msg = "你正常一点"
    await session.send(msg)
'''