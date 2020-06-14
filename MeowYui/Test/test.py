import requests
import ast
import json
import re
import time
from aiocqhttp import MessageSegment

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.97 Safari/537.36'
}
url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=399457732631781267'
html = requests.get(url, headers=headers)
html_content = ast.literal_eval(html.text)
#print(json.dumps(html_content, ensure_ascii=False, indent=4))
dynamic = json.dumps(html_content["data"]["card"]["card"])
dynamic = re.sub(r"\\+", r"\\", dynamic)
dynamic = dynamic.replace("\\\"", "\"")
dynamic = dynamic.replace("\\/", "/")
dynamic = dynamic.replace("null ", "None ")  # 由于返回数据中可能存在空值null，为了保持语义一致将其改为None
dynamic = dynamic.replace("null,", "None,")  # 由于返回数据中可能存在空值null，为了保持语义一致将其改为None
dynamic = dynamic.replace("false ", "False,")
dynamic = dynamic.replace("false,", "False,")
dynamic = dynamic.replace("true ", "True,")
dynamic = dynamic.replace("true,", "True,")
while re.search(r"(.*)(\"\{)(.*)(\}\")(.*)", dynamic) is not None:
    dynamic = re.sub(r"(.*)(\"\{)(.*)(\}\")(.*)", lambda x: x.group(1) + "{" + x.group(3) + "}" + x.group(5), dynamic)
while re.search(r"(.*)(\"\[)(.*)(\]\")(.*)", dynamic) is not None:
    dynamic = re.sub(r"(.*)(\"\[)(.*)(\]\")(.*)", lambda x: x.group(1) + "[" + x.group(3) + "]" + x.group(5), dynamic)
print(dynamic)
# print(ast.literal_eval(dynamic))
# print(json.dumps(ast.literal_eval(dynamic), ensure_ascii=False, indent=4))
dynamic_dict = ast.literal_eval(dynamic)
print(dynamic_dict)
print(json.dumps(dynamic_dict, ensure_ascii=False, indent=4))

fmt = "【B站动态推送-专栏转发】\n" + \
      dynamic_dict["user"]["uname"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
        html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
      dynamic_dict["item"]["content"] + "\n---------------------原专栏---------------------\n" + \
      dynamic_dict["origin"]["author"]["name"] + "\n" + "标题：" + dynamic_dict["origin"]["title"] + "\n" +\
      "专栏地址：bilibili.com/read/cv" + str(dynamic_dict["origin"]["id"]) + "\n" + "动态链接：t.bilibili.com/"
print(fmt)