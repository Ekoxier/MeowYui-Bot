import requests
from bs4 import BeautifulSoup
import ast
import json
import re
import time
#
# str="bilibili://video/583490570/?page=1&player_preload=null&player_width=1920&player_height=1080&player_rotate=0"
# video_url = "https://www.bilibili.com/video/" + re.search(r"(bilibili://video/)(\d+)(/*)", str).group(2)
# print(video_url)
