from datetime import datetime
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
import pytz


group = [319691773, 964997420]
bot = nonebot.get_bot()


@nonebot.scheduler.scheduled_job('cron', hour='0, 6')
async def _hour_call_a():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in group:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦！')
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', hour='12, 18')
async def _hour_call_b():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in group:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]已经{now.hour}点啦，へんたいさん记得去商店买经验药剂哦，别忘了体力任务也可以领取了！')
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', hour='5')
async def _hour_call_c():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    for i in group:
        try:
            await bot.send_group_msg(group_id=i,
                                     message=f'[日常提醒]已经{now.hour}点啦，今天又是没有mana的一天呢。')
        except CQHttpError:
            pass


@nonebot.scheduler.scheduled_job('cron', minute='*')
async def _hour_call_test():
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=319691773,
                                 message=f'[测试]现在是{now}。')
    except CQHttpError:
        pass
