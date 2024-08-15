import re
import requests
from wbinfosec.utils import handlefile

# 微博Cookie
wbcookie = 'SUB=_2AkMVrq79f8NxqwFRmP8dz2vqZYtwzAHEieKj8l8mJRMxHRl-yT9kqkMStRB6Pi6AElPJ4s5OahxIJazznHV8AyFL_V8w; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WFQQ4s24JbhxHkgOLHQ_3e6; SINAGLOBAL=6734641230168.771.1665654830067; UOR=,,www.pptstore.net; XSRF-TOKEN=Qn0phWQyvGXF1qjBBH4X_iUh; _s_tentry=-; Apache=1802076393369.6294.1682736373315; ULV=1682736373334:8:6:4:1802076393369.6294.1682736373315:1682668122294; ariaDefaultTheme=default; ariaFixed=true; ariaReadtype=1; ariaMouseten=null; ariaStatus=false; WBPSESS=dg5zs_KFY81p0FnDKmb34ZAbLLoCBaVSd_jWHWCoL3kepEXt4Los1pLePRcxA40HASLWb1Jv3UlVYCn5F06QUC2uwLp3CdBDKuK-sstjuuPYjwZT6wp7LftV72dHqXmosg9SexBzIRkOO3eNbUSelegYWNHps4Bhm5a69BhBRr8='
class Wbuser_info:
    # 用户编号
    id = ''
    # 用户名称
    screen = ''
    # 粉丝数量
    follow = ''
    # 用户地址
    location = ''
    # 用户性别
    gender = '未知'
    # 用户信用
    credit = ''
    # 浏览器cookie
    cookie = ''
    
    def __init__(self, custom = '2656274875', cookie = wbcookie):
        # 微博cookie
        self.cookie = cookie
        # 个人信息
        userinfo = self.userInfo(custom)
        self.id = userinfo['id']
        self.screen = userinfo['screen_name']
        self.follow = userinfo['followers_count_str']
        self.location = userinfo['location']
        self.gender = userinfo['gender']
        # 获取用户信誉
        credit_url = 'https://weibo.com/ajax/profile/detail?uid={custom}'.format(custom = custom)
        pretend = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'cookie': self.cookie}
        resp_credit = requests.get(credit_url, headers = pretend)
        text_credit = resp_credit.json()['data']['sunshine_credit']['level']
        self.credit = text_credit
    
    def userInfo(self, custom):
        '''
        爬取用户信息(爬取个人信息需要使用cookie)
        :param custom: 用户编号
        :return: 用户信息
        '''
        userinfo = {'id': '', 'screen_name': '', 'followers_count_str': '', 'location': '', 'gender': '未知'}
        userinfo_url = 'https://weibo.com/ajax/profile/info?custom={custom}'.format(custom = custom)
        pretend = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'cookie': self.cookie}
        resp_userinfo = requests.get(userinfo_url, headers = pretend)
        text_userinfo = resp_userinfo.json()['data']['user']
        for key in userinfo:
            if key in text_userinfo:
                userinfo[key] = text_userinfo[key]
        match userinfo['gender']:
            case 'm':
                userinfo['gender'] = '男性'
            case 'f':
                userinfo['gender'] = '女性'
        return userinfo
    
    def getWbuser(self):
        if self.id == ''  or self.screen == '':
            return None
        userinfo = {'id': self.id, 'screen': self.screen, 'follow': self.follow, 'location': self.location, 'gender': self.gender, 'credit': self.credit}
        return userinfo

class Wbuser:
    # 微博内容
    text = ''
    # 微博标号
    mid = ''
    mblog_id = ''
    # 微博评论
    comment = 0
    # 微博点赞
    attitude = 0
    # 浏览器cookie
    cookie = ''
    
    def __init__(self, blog, cookie = wbcookie):
        self.text = ''
        self.mid = ''
        self.mblog_id = ''
        self.comment = 0
        self.attitude = 0
        self.pic_url = []
        self.pic_len = 0
        # 微博cookie
        self.cookie = cookie
        if 'mblogid' in blog:
            self.mblog_id = blog['mblogid']
        if 'text' in blog:
            text_html = blog['text']
            need = self.needAll(text_html)
            self.text = self.getText(need)
        if 'mid' in blog:
            self.mid = blog['mid']
        if 'comments_count' in blog:
            self.comment = blog['comments_count']
        if 'attitudes_count' in blog:
            self.attitude = blog['attitudes_count']
    
    def needAll(self, text_html):
        '''
        对于内容只显示部分的评论爬取全文
        :param text_html: 初始评论
        :return: 返回全文
        '''
        needre = r'\.\.\.<span class="expand">展开</span>$'
        need = re.search(needre, text_html)
        if need is None or self.mblog_id == '':
            return text_html
        else:
            all_url = 'https://weibo.com/ajax/statuses/longtext?id={mblog_id}'.format(mblog_id = self.mblog_id)
            pretend = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'cookie': self.cookie}
            resp_all = requests.get(all_url, headers = pretend)
            text_all = resp_all.json()
            text_all = text_all['data']['longTextContent']
            return text_all
    
    def getText(self, text_html):
        '''
        将含有HTML标签的评论转化为纯字符串
        :param text_html: 含有HTML标签的字符串
        :return: 无HTML标签的字符串
        '''
        to_clean = re.compile('<.*?>|\\u200b')
        text = re.sub(to_clean, '', text_html)
        return text
        
    def getUser(self):
        if self.text is None:
            return None
        user = {'text': self.text, 'mid': self.mid, 'comment': self.comment, 'attitude': self.attitude, 'pic_url': self.pic_url, 'pic_len': self.pic_len}
        return user

def makehtml(custom = '2656274875', allnum = 20, cookie = wbcookie):
    allnum = int(allnum)
    # 请求页面
    page = 1
    # 博文总数
    count = 0
    tolist = []
    # 文件中首先包含用户信息
    wbuser_info = Wbuser_info(custom, cookie).getWbuser()
    if wbuser_info is None:
        return
    tolist.append(wbuser_info)
    while count < allnum:
        wbuser_url = 'https://weibo.com/ajax/statuses/mymblog?uid={uid}&page={page}&feature=0'.format(uid = custom, page = page)
        pretend = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36', 'cookie': cookie}
        resp_wbuser = requests.get(wbuser_url, headers = pretend)
        if 'data' in resp_wbuser.json():
            text_wbuser = resp_wbuser.json()['data']['list']
            # 防止用户内容过少
            if len(text_wbuser) <= 1:
                break
            for blog in text_wbuser:
                wbuser = Wbuser(blog)
                user = wbuser.getUser()
                if user is not None:
                    tolist.append(user)
                    count = count + 1
                    if count >= allnum:
                        break
        else:
            break
        page = page + 1
    fileta = 'wbfile/wbuser.json'
    handlefile.toFile(tolist, fileta)

def showfile():
    '''
    从.json文件中获取搜索结果
    :return: 文件内容
    '''
    fileta = 'wbfile/wbuser.json'
    wbsearch = handlefile.fromFile(fileta)
    return wbsearch

if __name__ == '__main__':
    makehtml()
