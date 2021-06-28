# -*- coding: utf8 -*-
import json
import time
import requests
import datetime


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded'
}


#哔哩哔哩频道id
bilibili_id = "53166650"
#rss的标题
rss_title = "晓涵哥来了"
#rss描述信息
rss_desc = "晓涵哥来了的个人空间_哔哩哔哩_Bilibili"


#unix时间转换为rss规则时间
def format_time(unixtime):
    dt = datetime.datetime.fromtimestamp(int(unixtime))
    offset = datetime.timedelta(hours=+8)
    timestr = (dt + offset).strftime('%a, %d %b %Y %H:%M:%S GMT')
    return timestr



def getRss():
    url = "https://api.bilibili.com/x/space/arc/search?mid=" + bilibili_id
    res = requests.get(url=url, headers=headers)
    code = json.loads(res.text)
    vlist = code.get('data').get('list').get('vlist')
    print(vlist)
    return vlist


def main_handler(event, context):
    res = getRss()

    body1 = '<?xml version="1.0" encoding="UTF-8" ?><rss version="2.0"><channel><title>' + rss_title + '</title><link>https://space.bilibili.com/' + bilibili_id + '</link><description>' + rss_desc + '</description><image><url>http://www.bilibili.com</url><title>' + rss_title + '</title><link>http://www.bilibili.com</link></image><language>zh-cn</language>'

    body2 = ""
    for s in res:
        body2 += '\n<item><pubDate>' + format_time(s.get('created')) + '</pubDate><title>' + s.get('title') + '</title><link>https://www.bilibili.com/video/' + s.get('bvid') + '</link><description><![CDATA[ <p><img  src="' + s.get('pic') + ' "/></p><p>' + s.get('description') + '</p> ]]></description></item>'
    body3 = '\n</channel>\n</rss>'

    body = body1 + body2 + body3

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {"Content-Type":"application/xml; charset=utf-8"},
        "body": body
    }
