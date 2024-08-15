import requests
import jieba
import base64
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO
from wbinfosec.utils import handlefile
from wordcloud import WordCloud

class Wbtop:
    '''
    微博热搜榜
    '''
    # 热搜类别
    category = ''
    # 热搜标题
    word = ''
    # 热搜热度值
    num = 0
    # 热搜链接
    top_url = ''
    # 是否是广告
    is_ad = 0
    
    def __init__(self, band):
        if 'is_ad' in band:
            self.is_ad = band['is_ad']
        if 'category' in band:
            self.category = band['category']
        if 'word' in band:
            self.word = band['word']
            # word_url = urllib.parse.quote(self.word)
            # self.top_url = 'https://s.weibo.com/weibo?q=%23{url_body}%23'.format(url_body = word_url)
            self.top_url = self.word
        if 'num' in band:
            self.num = band['num']
    
    def getTop(self):
        '''
        返回热搜信息
        :return: 热搜信息, 同时剔除广告
        '''
        if self.is_ad == 1:
            return None
        top = {'category': self.category, 'word': self.word, 'num': self.num, 'top_url': self.top_url}
        return top
    
def makehtml():
    wbtop_url = 'https://weibo.com/ajax/statuses/hot_band'
    pretend = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'}
    resp_wbtop = requests.get(wbtop_url, headers = pretend)
    text_wbtop = resp_wbtop.json()
    band_list = text_wbtop['data']['band_list']
    tolist = []
    for band in band_list:
        wbtop = Wbtop(band)
        top = wbtop.getTop()
        if top is not None:
            tolist.append(top)
    fileta = 'wbfile/wbtop.json'
    handle = handlefile.toFile(tolist, fileta)
    if handle is not None:
        print('文件路径错误')
        
def showfile():
    fileta = 'wbfile/wbtop.json'
    wbtop_list = handlefile.fromFile(fileta)
    return wbtop_list

def bar(hotnum):
    '''
    绘制微博热搜榜单的柱状图
    :param hotnum: 柱状图标签
    '''
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize = (10, 5))
    x_list = []
    y_list = []
    for cate in hotnum:
        x_list.append(cate)
        y_list.append(hotnum[cate])
    plt.bar(x_list, y_list)
    plt.xticks(x_list, x_list, rotation = 30)
    plt.title('微博热搜榜单话题类别柱状图')
    plt.xlabel('热搜分类')
    plt.ylabel('总热度值/万')
    pltbyte = BytesIO()
    plt.savefig(pltbyte, format = 'jpg', dpi = 300)
    imgbar = base64.encodebytes(pltbyte.getvalue()).decode()
    htmlbar = 'data:image/png;base64,' + str(imgbar)
    plt.close()
    return htmlbar

def pie(hotnum):
    '''
    绘制微博热搜榜单的扇形图
    :param hotnum: 扇形图标签
    '''
    plt.rcParams['font.sans-serif'] = 'SimHei'
    plt.rcParams['axes.unicode_minus'] = False
    size = []
    label = []
    for cate in hotnum:
        label.append(cate)
        size.append(hotnum[cate])
    plt.pie(size, labels = label, autopct = '%1.1f%%', shadow = False, startangle = 90)
    plt.axis('equal')
    pltbyte = BytesIO()
    plt.savefig(pltbyte, format = 'jpg', dpi = 300)
    imgpie = base64.encodebytes(pltbyte.getvalue()).decode()
    htmlpie = 'data:image/png;base64,' + str(imgpie)
    plt.close()
    return htmlpie

def cloud(word):
    '''
    生成微博热搜词云图, 背景为wbfile\cloudmask.jpg
    :param word: 热搜榜内容列表
    '''
    # 利用jieba库进行中文分词
    word_list = jieba.lcut(''.join(word))
    text = ' '.join(word_list)
    # 词云背景
    impt = handlefile.getPath('wbfile\cloudmask.jpg')
    cloudmask = mpimg.imread(impt)
    # 生成词云
    fopt = handlefile.getPath('wbfile\Deng.ttf')
    wordcloud = WordCloud(font_path = fopt, background_color = 'white', max_font_size = 200, min_font_size = 40,
                        mask = cloudmask, width = 1000, height = 860, scale = 1, margin = 2,).generate(text)
    plt.imshow(wordcloud)
    # 不显示坐标轴
    plt.axis('off')
    pltbyte = BytesIO()
    plt.savefig(pltbyte, format = 'jpg', dpi = 300)
    imgcloud = base64.encodebytes(pltbyte.getvalue()).decode()
    htmlcloud = 'data:image/png;base64,' + str(imgcloud)
    plt.close()
    return htmlcloud
