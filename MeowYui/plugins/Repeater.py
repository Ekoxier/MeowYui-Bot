import random
import nonebot

bot = nonebot.get_bot()
PROB_A = 1.6
group_stat = {}  # group_id: (last_msg, is_repeated, p)

'''
不复读率 随 复读次数 指数级衰减
从第2条复读，即第3条重复消息开始有几率触发复读

a 设为一个略大于1的小数，最好不要超过2，建议1.6
复读概率计算式：p_n = 1 - 1/a^n
递推式：p_n+1 = 1 - (1 - p_n) / a
'''


@bot.on_message('group')
async def random_repeater(context):
    group_id = context['group_id']
    msg = str(context['message'])

    if group_id not in group_stat:
        group_stat[group_id] = (msg, False, 0)
        return

    last_msg, is_repeated, p = group_stat[group_id]
    if last_msg == msg:  # 群友正在复读
        if not is_repeated:  # 机器人尚未复读过，开始测试复读
            if random.random() < p:  # 概率测试通过，复读并设flag
                    group_stat[group_id] = (msg, True, 0)
                    await bot.send(context, msg)
            else:  # 概率测试失败，蓄力
                p = 1 - (1 - p) / PROB_A
                group_stat[group_id] = (msg, False, p)
    else:  # 不是复读，重置
        group_stat[group_id] = (msg, False, 0)
