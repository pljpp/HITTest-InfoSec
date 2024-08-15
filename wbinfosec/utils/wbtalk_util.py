import re
import urllib
import requests
from wbinfosec.utils import handlefile


class Wbtalk:
    def __init__(self, card):
        self.mblog_id = ''
        self.scheme = ''
        self.text = ''
        self.pic_len = 0
        self.pic_url = []
        self.user_screen = ''
        self.user_url = ''
        if 'card_group' in card:
            card = card['card_group'][0]
        handle = self.handle_card(card)
        if handle is not None:
            mblog = handle[1]
            self.scheme = handle[0]
            if 'id' in mblog:
                self.mblog_id = mblog['id']
            if 'text' in mblog:
                text_html = mblog['text']
                need = self.needAll(text_html)
                self.text = self.getText(need)
            if 'pic_num' in mblog:
                if mblog['pic_num'] > 0:
                    # 图片数量: pic_num有时会大于len(mblog['pics]), 具体原因未知
                    self.pic_len = len(mblog['pics'])
                    for i in range(self.pic_len):
                        self.pic_url.append(mblog['pics'][i]['url'])
            if 'user' in mblog:
                user = mblog['user']
                if user is not None:
                    # 用户昵称
                    self.user_screen = user['screen_name']
                    # 用户主页链接
                    # self.user_url = user['profile_url']
                    if 'id' in user:
                        self.user_url = str(user['id'])
                    else:
                        self.user_url = '#'

    def handle_card(self, card):
        '''
        从话题卡片中提取信息
        :param card: 话题卡片
        :return: 对话题卡片提取的信息
        '''
        scheme = ''
        mblog = ''
        if not isinstance(card, dict):
            return None
        if 'scheme' in card:
            scheme = card['scheme']
            if 'mblog' in card:
                mblog = card['mblog']
            return (scheme, mblog)
        return None

    def needAll(self, text_html):
        '''
        对于内容只显示部分的评论爬取全文
        :param text_html: 初始评论
        :return: 返回全文
        '''
        needre = r'\.\.\.<a href=\"[^<>\"]+\">全文</a>$'
        need = re.search(needre, text_html)
        if need is None:
            return text_html
        else:
            all_url = 'https://m.weibo.cn/statuses/extend?id={mblog_id}'.format(mblog_id=self.mblog_id)
            pretend = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            resp_all = requests.get(all_url, headers=pretend)
            text_all = resp_all.json()
            text_all = text_all['data']['longTextContent']
            return text_all

    def getText(self, text_html):
        '''
        将含有HTML标签的评论转化为纯字符串
        :param text_html: 含有HTML标签的字符串
        :return: 无HTML标签的字符串
        '''
        to_clean = re.compile('<.*?>')
        text = re.sub(to_clean, '', text_html)
        return text

    def getPic(self):
        handlefile.picToFile(self.pic_url, self.mblog_id, 'wbfile/wbtalk_pic/')

    def getTalk(self):
        '''
        返回卡片信息
        :return: 话题卡片的信息
        '''
        if self.scheme == '' or self.scheme is None or self.user_screen is None or self.user_screen == '':
            return None
        card = {'scheme': self.scheme, 'mblog_id': self.mblog_id, 'text': self.text, 'pic_len': self.pic_len,
                'pic_url': self.pic_url, 'user_screen': self.user_screen, 'user_url': self.user_url}
        return card


def intourl(tourl):
    '''
    获取URL
    :param tourl: 需要转化为URL的字符串
    '''
    reurl = urllib.parse.quote(tourl)
    return reurl


def makehtml(search_content='哈尔滨工业大学', allnum=30):
    '''
    爬取输入话题的内容并写入文件, 选择爬取30条
    :param search_content: 搜索内容
    '''
    allnum = int(allnum)
    search_content = intourl(search_content)
    containerid = 100103
    # 请求页面
    page = 1
    # 评论总数
    count = 0
    tolist = []
    try:
        while count < allnum:
            wbtalk_url = 'https://m.weibo.cn/api/container/getIndex?containerid={containerid}type%3D1%26t%3D10%26q%3D{search_content}&page_type=searchall&page={page}'.format(
                containerid=containerid, search_content=search_content, page=page)
            pretend = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
            resp_wbtalk = requests.get(wbtalk_url, headers=pretend)
            text_wbtalk = resp_wbtalk.json()
            if 'data' in text_wbtalk:
                cards = text_wbtalk['data']['cards']
                # 防止话题内容过少
                if len(cards) <= 1:
                    break
                for card in cards:
                    wbtalk = Wbtalk(card)
                    getcard = wbtalk.getTalk()
                    if getcard is not None:
                        if len(getcard['pic_url']) > 0:
                            wbtalk.getPic()
                        tolist.append(getcard)
                        count = count + 1
                        if count >= allnum:
                            break
            else:
                break
            page = page + 1
    except Exception:
        tolist = []
    fileta = 'wbfile/wbtalk.json'
    handlefile.toFile(tolist, fileta)


def showfile():
    '''
    从.json文件中获取搜索结果
    :return: 文件内容
    '''
    fileta = 'wbfile/wbtalk.json'
    wbtalk = handlefile.fromFile(fileta)
    return wbtalk
