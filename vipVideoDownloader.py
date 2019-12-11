import sys

import utils

if __name__ == '__main__':
    utils.init()
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
        if len(sys.argv) > 2:
            dir = sys.argv[2]
    else:
        print("please input video url ! 【官网的播放页面】")
        print("such as https://v.qq.com/x/cover/3fvg46217gw800n.html、https://www.iqiyi.com/v_19rrfe142o.html")
        video_url = input(">...")
    utils.download(video_url)


