from nonebot import on_command, CommandSession
from datetime import datetime

import pytz
import nonebot
from aiocqhttp.exceptions import Error as CQHttpError


@on_command('在？', aliases='在?')
async def ping(session: CommandSession):
    await session.send('buzai')


@on_command('测试')
async def test(session: CommandSession):
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=964997420,
                                 message=f'[测试]现在是{now.hour}点{now.minute}分，今天的へんたいさん攒够一井了吗？')
        await bot.send_group_msg(group_id=319691773,
                                 message=f'[测试2]现在是{now.hour}点{now.minute}分，今天的へんたいさん攒够一井了吗？')
    except CQHttpError:
        pass