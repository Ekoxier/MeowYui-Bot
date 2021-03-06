from nonebot import on_command, CommandSession
import requests
import ast
import json
import re
import time
from aiocqhttp import MessageSegment
from aiocqhttp.exceptions import Error as CQHttpError
import nonebot
from group_list import groups


@nonebot.scheduler.scheduled_job('cron', minute='0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55', second='30')
async def dynamic_forward():
    count = 0
    print("【动态列表更新检查】 \n -------------------------")
    for x in uids:
        current_list = get_dynamic_ids(x)
        for y in range(0, len(current_list)):
            if latest_dynamic_of_uids[count] == current_list[y]:
                latest_dynamic_of_uids[count] = current_list[0]
                new = y
                if y == 0:
                    print(str(uids[x]) + ": None")
                else:
                    print(str(uids[x]) + ": " + str(new) + " New")
                for z in range(0, y):
                    for j in groups:
                        try:
                            await bot.send_group_msg(group_id=j,
                                                     message=get_dynamic_content(current_list[z]) + str(
                                                         current_list[z]))
                        except CQHttpError:
                            pass
                break
        count = count + 1
    print("-------------------------")


@on_command('动态获取测试')
async def user_dynamic_test(session: CommandSession):
    dynamic_id_list = get_dynamic_ids(session.get('uid'))
    for i in range(0, 3):
        msg = get_dynamic_content(dynamic_id_list[i]) + str(dynamic_id_list[i])
        print(msg)
        await session.send(msg)


@user_dynamic_test.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['uid'] = stripped_arg
        return


@on_command('动态', aliases=('b站动态', 'B站动态'))
async def dynamic_test(session: CommandSession):
    dynamic_id = session.get('dynamic_id')
    msg = get_dynamic_content(dynamic_id) + str(dynamic_id)
    print("【动态推送】Push dynamic " + str(dynamic_id) + " successful!")
    await session.send(msg)


@dynamic_test.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['dynamic_id'] = stripped_arg
        return


def get_dynamic_ids(uid):
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=" + str(uid)
    html = requests.get(url)
    # print(html.text)
    desc_lists = html.json()['data']['cards']
    arr = []
    for dynamic in desc_lists:
        arr.append(dynamic['desc']['dynamic_id'])
    # print(arr[0:5])
    return arr


def get_dynamic_content(dynamic_id):
    # 获取动态内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36'
    }
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=' + str(dynamic_id)
    html = requests.get(url, headers=headers)
    html_content = ast.literal_eval(html.text)

    # 动态内容格式解析部分
    dynamic = json.dumps(html_content['data']['card']['card'])
    dynamic = re.sub(r"\\+", r"\\", dynamic)
    dynamic = dynamic.replace("\\\"", "\"")
    dynamic = dynamic.replace("\\/", "/")
    dynamic = dynamic.replace("null ", "None ")  # 由于返回数据中可能存在空值null，为了保持语义一致将其改为None
    dynamic = dynamic.replace("null,", "None,")  # 由于返回数据中可能存在空值null，为了保持语义一致将其改为None
    dynamic = dynamic.replace("false ", "False,")
    dynamic = dynamic.replace("false,", "False,")
    dynamic = dynamic.replace("true ", "True,")
    dynamic = dynamic.replace("true,", "True,")
    while re.search(r"(.*)(\"{)(.*)(\}\")(.*)", dynamic) is not None:
        dynamic = re.sub(r"(.*)(\"{)(.*)(\}\")(.*)", lambda x: x.group(1) + "{" + x.group(3) + "}" + x.group(5),
                         dynamic)
    while re.search(r"(.*)(\"\[)(.*)(\]\")(.*)", dynamic) is not None:
        dynamic = re.sub(r"(.*)(\"\[)(.*)(\]\")(.*)", lambda x: x.group(1) + "[" + x.group(3) + "]" + x.group(5),
                         dynamic)
    dynamic_dict = ast.literal_eval(dynamic)  # 转换为字典格式

    # 组装消息
    content_max_length = 1000  # 正文长度上限
    origin_max_length = 100  # 原动态长度上限
    # 动态类型-分享游戏
    if dynamic_dict.get("vest") is not None:
        cover_url = dynamic_dict["sketch"]["cover_url"]
        content = dynamic_dict["vest"]["content"]
        if len(content) > content_max_length:
            content = content[0:content_max_length] + "……"
        fmt = "【B站动态推送-游戏分享】\n" + \
              dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
              content + "\n------------------------------------------------\n" + \
              dynamic_dict["sketch"]["title"] + "\n" + dynamic_dict["sketch"]["desc_text"] + "\n" + \
              str(MessageSegment.image(cover_url)) + "\n" + "动态地址：t.bilibili.com/"
    # 动态类型-视频投稿
    elif dynamic_dict.get("owner") is not None:
        img_url = dynamic_dict["pic"]
        video_url = "https://www.bilibili.com/video/av" + str(dynamic_dict["aid"])
        fmt = "【B站动态推送-视频投稿】\n" + \
              dynamic_dict["owner"]["name"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
              dynamic_dict["desc"] + "\n------------------------------------------------\n" + \
              "视频地址：" + dynamic_dict["title"] + "\n" + "视频地址：" + video_url + "\n" + \
              str(MessageSegment.image(img_url)) + "\n" + \
              "动态地址：t.bilibili.com/"
    # 动态类型-专栏投稿
    elif dynamic_dict.get("author") is not None:
        fmt = "【B站动态推送-专栏投稿】\n" + \
              dynamic_dict["author"]["name"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + "专栏标题：" + dynamic_dict["title"] + "\n" + \
              "专栏地址：bilibili.com/read/cv" + str(dynamic_dict["id"]) + "\n" + "动态地址：t.bilibili.com/"
    # 动态类型-原创内容
    elif dynamic_dict.get("origin") is None:
        # 无图
        if dynamic_dict["item"].get("content") is not None:
            content = dynamic_dict["item"]["content"]
            if len(content) > content_max_length:
                content = content[0:content_max_length] + "……"
            fmt = "【B站动态推送-原创内容】\n" + \
                  dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                  content + "\n" + "动态地址：t.bilibili.com/"
        # 有图
        else:
            img_url = dynamic_dict["item"]["pictures"][0]["img_src"]
            content = dynamic_dict["item"]["description"]
            if len(content) > content_max_length:
                content = content[0:content_max_length] + "……"
            fmt = "【B站动态推送-原创内容】\n" + \
                  dynamic_dict["user"]["name"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                  content + "\n" + str(MessageSegment.image(img_url)) + "\n" + \
                  "共" + str(dynamic_dict["item"]["pictures_count"]) + "张图片，详情点击下方链接" + "\n" + \
                  "动态地址：t.bilibili.com/"

    else:
        # 动态类型 - 动态转发
        if dynamic_dict["origin"].get("item") is not None:
            # 有图
            if dynamic_dict["origin"]["item"].get("pictures") is not None:
                img_url = dynamic_dict["origin"]["item"]["pictures"][0]["img_src"]
                content = dynamic_dict["item"]["content"]
                if len(content) > content_max_length:
                    content = content[0:content_max_length] + "……"
                origin = dynamic_dict["origin"]["item"]["description"]
                if len(origin) > origin_max_length:
                    origin = origin[0:origin_max_length] + "……"
                fmt = "【B站动态推送-动态转发】\n" + \
                      dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                      content + "\n------------------------------------------------\n" + \
                      dynamic_dict["origin"]["user"]["name"] + "\n" + \
                      origin + "\n" + \
                      str(MessageSegment.image(img_url)) + "\n" + \
                      "共" + str(dynamic_dict["origin"]["item"]["pictures_count"]) + "张图片，详情点击下方链接" + "\n" + \
                      "动态地址：t.bilibili.com/"
            # 无图
            else:
                content = dynamic_dict["item"]["content"]
                if len(content) > content_max_length:
                    content = content[0:content_max_length] + "……"
                origin = dynamic_dict["origin"]["item"]["content"]
                if len(origin) > origin_max_length:
                    origin = origin[0:origin_max_length] + "……"
                fmt = "【B站动态推送-动态转发】\n" + \
                      dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                      content + "\n------------------------------------------------\n" + \
                      dynamic_dict["origin"]["user"]["uname"] + "\n" + origin + "\n" + \
                      "动态地址：t.bilibili.com/"
        # 动态类型-专栏转发\视频分享
        else:
            # 专栏转发
            if dynamic_dict["origin"].get("author") is not None:
                content = dynamic_dict["item"]["content"]
                if len(content) > content_max_length:
                    content = content[0:content_max_length] + "……"
                fmt = "【B站动态推送-专栏转发】\n" + \
                      dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                      content + "\n------------------------------------------------\n" + \
                      dynamic_dict["origin"]["author"]["name"] + "\n" + \
                      "专栏标题：" + dynamic_dict["origin"]["title"] + "\n" + \
                      "专栏地址：bilibili.com/read/cv" + str(dynamic_dict["origin"]["id"]) + "\n" + "动态地址：t.bilibili.com/"
            # 视频分享
            else:
                img_url = dynamic_dict["origin"]["pic"]
                video_url = "https://www.bilibili.com/video/av" + re.search(r"(bilibili://video/)(\d+)(/*)",
                                                                            dynamic_dict["origin"]["jump_url"]).group(2)
                content = dynamic_dict["item"]["content"]
                if len(content) > content_max_length:
                    content = content[0:content_max_length] + "……"
                fmt = "【B站动态推送-视频转发】\n" + \
                      dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                      content + "\n------------------------------------------------\n" + \
                      dynamic_dict["origin_user"]["info"]["uname"] + "\n" + \
                      "视频标题：" + dynamic_dict["origin"]["title"] + "\n" + \
                      "视频地址：" + video_url + "\n" + \
                      str(MessageSegment.image(img_url)) + "\n" + "动态地址：t.bilibili.com/"
    fmt = fmt.replace("https://", "")
    fmt = fmt.replace("动态地址：", "动态地址：https://")
    fmt = fmt.replace("[CQ:image,file=", "[CQ:image,file=https://")
    return fmt


uids = {49458759: "乐爷Official",
        353840826: "公主连结ReDive",
        14454663: "席巴鸽",
        9135820: "盐取shiotori",
        13504140: "1s-rock",
        865683: "待宵姫Channel"}
bot = nonebot.get_bot()
latest_dynamic_of_uids = []
print("【动态列表初始化】", end="")
for user_uid in uids:
    latest_dynamic_of_uids.append(get_dynamic_ids(user_uid)[0])
print(" OK")
