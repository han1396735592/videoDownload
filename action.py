import utils
import requests
import json
import re
import m3u8


def download(opt):
    print("{:-<50}{:-^100}{:-<50}".format('-', 'download', '-'))
    print("参数: %s" % opt)
    print("-" * 200)
    if opt[1].startswith("http"):
        utils.download(opt[1])
    else:
        try:
            flag = re.match(r'\d+', opt[1])
            detail = getDetail(flag.string)
            config = utils.getConfig()
            # print()
            m3u8Map = dict()
            plays = detail['list'][0]['vod_play_url']
            index = str(str(plays)).find('#')
            if index > 0:
                ls = str(plays).split("#")
            else:
                ls = str(plays).split("$$$")
            for s in ls:
                print(s)
                if (s.endswith(".m3u8")):
                    ss = s.split('$')
                    m3u8Map[ss[0]] = ss[1]

            if len(m3u8Map.keys()) == 1:
                print(config['savePath'])
                m3u8.main([m3u8Map.popitem()[1]], config['savePath'], detail['list'][0]['vod_name'])
            else:
                urlList = list()
                dirList = list()
                titleList = list()
                index = str(opt[2]).find('-')
                if index > 0:
                    aa = opt[2].split('-')
                    for k in range(int(aa[0]), int(aa[1]) + 1):
                        titleList.append('第{}集'.format("0" * (len(aa) - len(str(k))) + str(k)))
                else:
                    aa = str(opt[2]).split(',')
                    for k in aa:
                        titleList.append('第%s集' % k)
                print("下载视频")
                print(titleList)
                for k in titleList:
                    # print(k)
                    dirList.append(config['savePath'] + detail['list'][0]['vod_name'])
                    urlList.append(m3u8Map[k])
                m3u8.main(urlList, dirList, titleList)
        except:
            print("参数有误")


def search(opt):
    print("{:-<50}{:-^100}{:-<50}".format('-', 'search', '-'))
    print("参数: %s" % opt)
    showList(getList(opt[1])['list'])
    print("-" * 200)


def detail(opt):
    print("{:-<50}{:-^20}{:-<50}".format('-', 'detail', '-'))
    print("参数: %s" % opt)
    data = getDetail(opt[1])
    showVod(data['list'][0])
    print("-" * 200)


def showVod(data):
    print("-------------%s-------------" % data['vod_name'])
    print("介绍:%s" % data['vod_content'])
    plays = data['vod_play_url']
    index = str(str(plays)).find('#')
    if index > 0:
        ls = str(plays).split("#")
    else:
        ls = str(plays).split("$$$")
    onlineMap = dict()
    m3u8Map = dict()
    mp4Map = dict()
    for s in ls:
        if (s.endswith(".m3u8")):
            ss = s.split('$')
            m3u8Map[ss[0]] = ss[1]
        elif (s.endswith(".mp4")):
            ss = s.split('$')
            mp4Map[ss[0]] = ss[1]
        else:
            ss = s.split('$')
            onlineMap[ss[0]] = ss[1]
    # print("在线观看:%s" % onlineMap)
    # print("m3u8地址:%s" % m3u8Map)
    # print("mp4地址:%s" % mp4Map)
    for k in m3u8Map:
        try:
            url = onlineMap[k]
        except:
            url = 'Null'
        print("{:<8}{:<96}{:<96}".format(k, m3u8Map[k],url))


def showList(data):
    print("{:<7}{:^30}{:^10}{:^12}".format("vod_id", "vod_name", 'type', 'time'))
    for row in data:
        print("{:<7}{:^30}{:^10}{:^12}".format(row['vod_id'], row['vod_name'], row['type_name'], row['vod_time']))


def getDetail(id):
    details = utils.getConfig()['jx']['detail']
    url = details + "&ids=" + id
    res = requests.get(url).text
    return json.loads(res)


def getList(wd):
    listUrl = utils.getConfig()['jx']['list']
    url = listUrl + "&wd=" + wd
    res = requests.get(url).text
    return json.loads(res)


def getM3u8Map(id):
    detail = getDetail(id)
    m3u8Map = dict()
    plays = detail['list'][0]['vod_play_url']
    index = str(str(plays)).find('#')
    if index > 0:
        ls = str(plays).split("#")
    else:
        ls = str(plays).split("$$$")
    for s in ls:
        if (s.endswith(".m3u8")):
            ss = s.split('$')
            m3u8Map[ss[0]] = ss[1]
    return m3u8Map
