from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError


@nonebot.scheduler.scheduled_job('cron', hour='0, 6')
async def _hour_call_a():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=964997420,
                                 message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦！')
        await bot.send_group_msg(group_id=319691773,
                                 message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦！')
        await bot.send_group_msg(group_id=1105438615,
                                 message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦！')
    except CQHttpError:
        pass


@nonebot.scheduler.scheduled_job('cron', hour='12, 18')
async def _hour_call_b():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=964997420,
                                 message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦，别忘了体力任务也可以领取了！')
        await bot.send_group_msg(group_id=319691773,
                                 message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦，别忘了体力任务也可以领取了！')
        await bot.send_group_msg(group_id=1105438615,
                                 message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦，别忘了体力任务也可以领取了！')
    except CQHttpError:
        pass


@nonebot.scheduler.scheduled_job('cron', hour='5')
async def _hour_call_c():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=964997420,
                                 message=f'[日常提醒]已经{now.hour}点啦，今天又是没有mana的一天呢。')
        await bot.send_group_msg(group_id=319691773,
                                 message=f'[日常提醒]已经{now.hour}点啦，今天又是没有mana的一天呢。')
        await bot.send_group_msg(group_id=1105438615,
                                 message=f'[日常提醒]已经{now.hour}点啦，今天又是没有mana的一天呢。')
    except CQHttpError:
        pass
