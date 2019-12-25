import os

from subprocess import call,Popen

import requests
import re
import time
import m3u8
import json

debug = False
def getConfig():
    if debug:
        file = open('./config.json', 'r')
        jsonStr = str(file.read())
    else:
        res = requests.get("https://gitee.com/han1396735592/videoDownload/raw/master/config.json")
        jsonStr = res.text
        # print("#" * 50)
        # print(jsonStr)
        # print("#" * 50)
    return json.loads(jsonStr)


def init():
    config = getConfig()
    global savePath
    savePath = config['savePath']
    global apis
    apis = config['apis']

def getM3u8Url(video_url):
    url = ''
    for api in apis:
        res = requests.get(api['api'] + video_url)
        li = re.findall(api['reg'], res.text)
        # print(li)
        if len(li) > 0:
            temp = "%s.m3u8" % li[0]
        if temp:
            url = temp
            break
    return url


def download(video_url):
    m3u8Url = getM3u8Url(video_url)
    title = getTitle(video_url)
    print("video url = " + video_url)
    print("save directory at  " + savePath)
    print("download video is  " + title)
    m3u8.main([m3u8Url], [savePath], [title])


def getTitle(video_url):
    if str(video_url).endswith('.m3u8'):
        return 'video-%s' % time.strftime('%Y-%m-%d%H:%M:%S')
    res = requests.get(video_url)
    title = re.findall(r"<title>(.+?)</title>", res.text)[0]
    return str(title).encode(res.encoding + "").decode("utf-8")
