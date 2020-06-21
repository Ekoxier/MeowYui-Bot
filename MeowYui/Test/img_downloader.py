# coding: utf8
import requests

'''
def download_img(img_url):
    print(img_url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.97 Safari/537.36'
    }
    r = requests.get(img_url, headers=headers, stream=True)
    print(r.status_code) # 返回状态码
    if r.status_code == 200:
        open('./img.jpg', 'wb').write(r.content) # 将内容写入图片
        print("done")
    del r


img_url = "https://www.baidu.com/img/flexible/logo/pc/result.png"
download_img(img_url)
'''