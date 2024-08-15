import re
import requests
from wbinfosec.utils import handlefile

wbcookie = 'TODO'


class Wbcomment:
    # 用户名称
    screen = ''
    # 用户编号
    uid = ''
    # 评论编号
    mid = ''
    # 评论地址
    source = ''
    # 评论内容
    text = ''

    def __init__(self, comment):
        if 'mid' in comment:
            self.mid = comment['mid']
        if 'source' in comment:
            self.source = comment['source']
        if 'text' in comment:
            self.text = self.getText(comment['text'])
        if 'user' in comment:
            user = comment['user']
            if 'id' in user:
                self.uid = str(user['id'])
            if 'screen_name' in user:
                self.screen = user['screen_name']

    def getText(self, text_html):
        '''
        将含有HTML标签的评论转化为纯字符串
        :param text_html: 含有HTML标签的字符串
        :return: 无HTML标签的字符串
        '''
        to_clean = re.compile('<.*?>|\\u200b')
        text = re.sub(to_clean, '', text_html)
        return text

    def getWbcomment(self):
        if self.uid != '' and self.mid != '':
            wbcomment = {'screen': self.screen, 'uid': self.uid, 'mid': self.mid, 'source': self.source,
                         'text': self.text}
            return wbcomment
        return None


def makehtml(mblogid, cookie=wbcookie):
    wbcomment_url = 'https://m.weibo.cn/comments/hotflow?id={mblogid}&mid={mblogid}&max_id_type=0'.format(
        mblogid=mblogid)
    pretend = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
        'cookie': cookie}
    try:
        # 无评论
        resp_wbcomment = requests.get(wbcomment_url, headers=pretend)
        text_wbcomment = resp_wbcomment.json()['data']['data']
        tolist = []
        for text_for in text_wbcomment:
            wbcomment = Wbcomment(text_for)
            comment_for = wbcomment.getWbcomment()
            if wbcomment is not None:
                tolist.append(comment_for)
    except Exception:
        tolist = []
    fileta = 'wbfile/wbcomment.json'
    handlefile.toFile(tolist, fileta)


def showfile():
    '''
    从.json文件中获取搜索结果
    :return: 文件内容
    '''
    fileta = 'wbfile/wbcomment.json'
    wbcomment = handlefile.fromFile(fileta)
    return wbcomment

