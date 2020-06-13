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
url = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/get_dynamic_detail?dynamic_id=399539345597531281'
html = requests.get(url, headers=headers)
html_content = ast.literal_eval(html.text)
print(json.dumps(html_content, ensure_ascii=False, indent=4))
dynamic = json.dumps(html_content["data"]["card"]["card"])
dynamic = re.sub(r"\\+", r"\\", dynamic)
dynamic = dynamic.replace("\\\"", "\"")
dynamic = dynamic.replace("\\/", "/")
dynamic = dynamic.replace("null,", "None,")  # 由于返回数据中可能存在空值null，为了保持语义一致将其改为None
while re.search(r"(.*)(\"\{)(.*)(\}\")(.*)", dynamic) is not None:
    dynamic = re.sub(r"(.*)(\"\{)(.*)(\}\")(.*)", lambda x: x.group(1) + "{" + x.group(3) + "}" + x.group(5), dynamic)
while re.search(r"(.*)(\"\[)(.*)(\]\")(.*)", dynamic) is not None:
    dynamic = re.sub(r"(.*)(\"\[)(.*)(\]\")(.*)", lambda x: x.group(1) + "[" + x.group(3) + "]" + x.group(5), dynamic)
# print(dynamic)
# print(ast.literal_eval(dynamic))
print(json.dumps(ast.literal_eval(dynamic), ensure_ascii=False, indent=4))
dynamic_dict = ast.literal_eval(dynamic)
#print(dynamic_dict)
'''
img_url = dynamic_dict["item"]["pictures"][0]["img_src"]
fmt = dynamic_dict["user"]["name"] + " " + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(
    html_content["data"]["card"]["desc"]["timestamp"])) + "\n" + \
    dynamic_dict["item"]["description"] + "\n" + MessageSegment.image(img_url) + "\n" +\
    "共" + str(dynamic_dict["item"]["pictures_count"]) + "张图片，详情点击下方链接" + "\n" +\
    "原文链接：https://t.bilibili.com/"
print(fmt)
'''