'''
处理文件
'''
import json
import requests
from os import path

def getPath(fileta):
    '''
    获取文件路径
    :return: 文件路径
    '''
    nowpath = path.dirname(__file__)
    jsonpath = path.join(nowpath, fileta)
    return jsonpath

def toFile(tolist, fileta):
    '''
    将列表内容写入.json文件
    :param tolist: 准备写入.json文件的列表
    :param fileta: 文件路径末尾
    :return: None; 或文件打开异常返回文件末尾
    '''
    filept = getPath(fileta)
    try:
        fileop = open(filept, 'w', encoding = 'UTF-8')
        json.dump(tolist, fileop)
        fileop.close()
        return None
    except Exception:
        return fileta

def fromFile(fileta):
    '''
    从.json文件中读取内容并转化为列表形式
    :param fileta: 文件末尾
    :return: 从文件中读取的列表内容; 或文件打开异常返回None
    '''
    filept = getPath(fileta)
    try:
        fileop = open(filept, 'r', encoding = 'UTF-8')
        fromlist = json.load(fileop)
        fileop.close()
        return fromlist
    except Exception:
        return None

def picToFile(tolist, mblogid, fileta):
    pic_name = 1
    for pic_for in tolist:
        resp_pic = requests.get(pic_for)
        picta = fileta + mblogid + '_' + str(pic_name) + '.jpg'
        pic_name = pic_name + 1
        filept = getPath(picta)
        try:
            fileop = open(filept, 'wb')
            fileop.write(resp_pic.content)
            resp_pic.close()
            fileop.close()
        except Exception:
            resp_pic.close()
            return False
    return True
