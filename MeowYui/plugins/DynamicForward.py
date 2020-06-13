from nonebot import on_command, CommandSession
import requests
import ast
import json
import re
import time
from aiocqhttp import MessageSegment


@on_command('动态', aliases='b站动态, B站动态')
async def dynamic_forward(session: CommandSession):
    dynamic_id = session.get('dynamic_id')
    msg = "【B站动态推送】\n" + get_dynamic_content(dynamic_id) + dynamic_id
    print(msg)
    await session.send(msg)


@dynamic_forward.args_parser
async def _(session: CommandSession):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()

    if session.is_first_run:
        if stripped_arg:
            session.state['dynamic_id'] = stripped_arg
        return

def get_dynamic_ids():
    url = "https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid=10330740"
    html = requests.get(url)
    desc_lists = html.json()['data']['cards']
    arr = []
    for list in desc_lists:
        arr.append(list['desc']['dynamic_id'])
    return arr

def get_dynamic_content(dynamic_id):
    # 获取动态内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36'
    }
    url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=' + dynamic_id
    html = requests.get(url, headers=headers)
    html_content = ast.literal_eval(html.text)

    # 动态内容格式解析部分
    dynamic = json.dumps(html_content['data']['card']['card'])
    dynamic = re.sub(r"\\+", r"\\", dynamic)
    dynamic = dynamic.replace("\\\"", "\"")
    dynamic = dynamic.replace("\\/", "/")
    dynamic = dynamic.replace("null,", "None,")  # 由于返回数据中可能存在空值null，为了保持语义一致将其改为None
    while re.search(r"(.*)(\"{)(.*)(\}\")(.*)", dynamic) is not None:
        dynamic = re.sub(r"(.*)(\"{)(.*)(\}\")(.*)", lambda x: x.group(1) + "{" + x.group(3) + "}" + x.group(5),
                         dynamic)
    while re.search(r"(.*)(\"\[)(.*)(\]\")(.*)", dynamic) is not None:
        dynamic = re.sub(r"(.*)(\"\[)(.*)(\]\")(.*)", lambda x: x.group(1) + "[" + x.group(3) + "]" + x.group(5),
                         dynamic)
    dynamic_dict = ast.literal_eval(dynamic)  # 转换为字典格式

    # 组装消息
    # 动态类型-分享游戏
    if dynamic_dict.get("vest") is not None:
        cover_url = dynamic_dict["sketch"]["cover_url"]
        fmt = dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
            html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
            dynamic_dict["vest"]["content"] + "\n------------------------------------------------\n" + \
            dynamic_dict["sketch"]["title"] + "\n" + dynamic_dict["sketch"]["desc_text"] + "\n" + \
            MessageSegment.image(cover_url) + "\n" + "原文链接：https://t.bilibili.com/"
        return fmt
    # 动态类型-原创
    elif dynamic_dict.get("origin") is None:
        # 无图
        if dynamic_dict["item"].get("content") is not None:
            fmt = dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                dynamic_dict["item"]["content"] + "\n" + "原文链接：https://t.bilibili.com/"
        # 有图
        else:
            img_url = dynamic_dict["item"]["pictures"][0]["img_src"]
            fmt = dynamic_dict["user"]["name"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                dynamic_dict["item"]["description"] + "\n" + MessageSegment.image(img_url) + "\n" + \
                "共" + str(dynamic_dict["item"]["pictures_count"]) + "张图片，详情点击下方链接" + "\n" + \
                "原文链接：https://t.bilibili.com/"

    else:
        # 动态类型 - 转发动态
        if dynamic_dict["origin"].get("item") is not None:
            # 有图
            if dynamic_dict["origin"]["item"].get("pictures") is not None:
                img_url = dynamic_dict["origin"]["item"]["pictures"][0]["img_src"]
                fmt = dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                    dynamic_dict["item"]["content"] + "\n------------------------------------------------\n" + \
                    dynamic_dict["origin"]["user"]["name"] + "\n" + dynamic_dict["origin"]["item"]["description"] + "\n" + \
                    MessageSegment.image(img_url) + "\n" + "原文链接：https://t.bilibili.com/"
            # 无图
            else:
                fmt = dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                    dynamic_dict["item"]["content"] + "\n------------------------------------------------\n" + \
                    dynamic_dict["origin"]["user"]["uname"] + "\n" + dynamic_dict["origin"]["item"]["content"] + "\n" +\
                    "原文链接：https://t.bilibili.com/"
        # 动态类型-分享视频
        else:
            img_url = dynamic_dict["origin"]["pic"]
            video_url = video_url = "https://www.bilibili.com/video/av" + re.search(r"(bilibili://video/)(\d+)(/*)", dynamic_dict["origin"]["jump_url"]).group(2)
            fmt = dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
                html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
                dynamic_dict["item"]["content"] + "\n------------------------------------------------\n" + \
                dynamic_dict["origin_user"]["info"]["uname"] + "\n" + "视频投稿：" + dynamic_dict["origin"]["title"] + "\n" + \
                "视频地址：" + video_url + "\n" +\
                MessageSegment.image(img_url) + "\n" + "原文链接：https://t.bilibili.com/"
    return fmt
