from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import pytz

from group_list import groups


bot = nonebot.get_bot()


@nonebot.scheduler.scheduled_job('cron', hour='0, 6')
async def _hour_call_a():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in groups:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦！')
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', hour='12, 18')
async def _hour_call_b():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in groups:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦，别忘了体力任务也可以领取了！')
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', hour='5')
async def _hour_call_c():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in groups:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]已经{now.hour}点啦，今天又是没有mana的一天呢。')
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', hour='14', minute='45')
async def _hour_call_d():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in groups:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]へんたいさん、准备好背刺了吗？')
        except CQHttpError:
            pass
