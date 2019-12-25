import utils
import action
import keyMap
def help():
    print("{:-<50}{:-^20}{:-<50}".format('-','help','-'))
    print("用法: 命令 + 参数")
    for key in keyMap.keyMap:
        print("{:<40} {:<30}".format(key['cmd'],key['description']))
    print("-"*120)
    readCmd()

def readCmd():
    cmd = list(map(str,input('请输入命令\n>..').split()))
    # print(cmd)
    if(len(cmd)>0):
        for key in keyMap.keyMap:
            keyWord = key['cmd'].split(' ')[0]
            if(cmd[0]==keyWord):
                eval('action.%s' % key['method'])(cmd)
                break
    else:
        print("输入命令有误\n")
        help()


if __name__ == '__main__':
    utils.init()
    while(True):
        help()


