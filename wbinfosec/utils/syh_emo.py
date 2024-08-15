import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64


def emojd(text):
    '''
    通过讯飞平台识别文本情感
    :param text:文本
    :return:文本分类:{-1:贬义;0:中性;1:褒义}
    '''
    # 接口地址
    url = "http://ltpapi.xfyun.cn/v2/sa"
    # 开放平台应用ID
    x_appid = "8b670553"
    # 开放平台应用接口秘钥
    api_key = "9606ec7e684266af16e76e3a4f818406"
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') + str(x_time).encode('utf-8') + x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    try:
        req = urllib.request.Request(url, body, x_header)
        result = urllib.request.urlopen(req)
        result = eval(result.read().decode('utf-8'))
    except Exception:
        result = None
    return result

