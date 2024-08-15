# @PydevCodeAnalysisIgnore
import os
from django.shortcuts import render, redirect
from wbinfosec.utils import wbtop_util, wbtalk_util, wmmatch, syh_imgre, handlefile
from wbinfosec.utils import syh_talk, syh_report, syh_emo

'''
from snownlp import SnowNLP
from snownlp import sentiment
'''

def new(request):
    '''
    爬取微博搜索内容
    :param request:
    '''
    if request.method == 'GET':
        need_id = request.GET.get('need_id')
        if need_id is None:
            return render(request, 'infosec_need.html')
        else:
            need_id = '#' + need_id + '#'
            need_num = 30
    elif request.method == 'POST':
        need_id = request.POST.get('need_id')
        need_num = request.POST.get('need_num')
        if int(need_num) <= 0:
            return render(request, 'infosec_need.html')
    wbtalk_util.makehtml(need_id, need_num)
    wbtalk_list = wbtalk_util.showfile()
    return render(request, 'wbtalk_new.html', {'wbtalk_list': wbtalk_list})

def show(request):
    '''
    微博热搜话题内容匹配结果
    :param request:
    '''
    if request.method == 'GET':
        wbtalk_list = wbtalk_util.showfile()
        # WM算法匹配违规词汇
        mode = badword()
        wm = wmmatch.DHSWM(mode)
        for wbtalk_for in wbtalk_list:
            mate = []
            wmresult = wm.search(wbtalk_for['text'])
            for forwm in wmresult:
                # 获取违规词个数
                if len(wmresult[forwm]) > 0:
                    mate.append((forwm, len(wmresult[forwm])))
            if mate == []:
                mate = ['None']
            wbtalk_for['mate'] = mate
            # wbtalk_for['emo'] = emoju(wbtalk_for['text'])
            emo = syh_emo.emojd(wbtalk_for['text'])
            if emo is None:
                wbtalk_for['emo'] = 'None'
            elif isinstance(emo, dict):
                # 讯飞执行参数有要求
                desc = emo['desc']
                if desc != 'success':
                    print('讯飞文本识别非法字符')
                    wbtalk_for['emo'] = '2'
                else:
                    emodt = emo['data']
                    if 'sentiment' in emodt:
                        wbtalk_for['emo'] = str(emodt['sentiment'])
                    else:
                        wbtalk_for['emo'] = '2'
            else:
                wbtalk_for['emo'] = '程序错误'
        return render(request, 'wbtalk_show.html', {'wbtalk_list': wbtalk_list})

def text(request):
    '''
    短语搜索
    :param request:
    '''
    if request.method == 'GET':
        wbtalk_list = 'None'
    # 接收用户输入的模式串集合, 应该以空格作为分隔
    elif request.method == 'POST':
        modes = request.POST.get('modes')
        mode = modes.split(' ')
        wm = wmmatch.DHSWM(mode)
        wbtalk_list = wbtalk_util.showfile()
        for wbtalk_for in wbtalk_list:
            mate = []
            wmresult = wm.search(wbtalk_for['text'])
            print(wmresult)
            for forwm in wmresult:
                # 获取违规词个数
                if len(wmresult[forwm]) > 0:
                    mate.append((forwm, len(wmresult[forwm])))
            if mate == []:
                mate = ['None']
            wbtalk_for['mate'] = mate
    for i in wbtalk_list:
        print(i['mate'])
    return render(request, 'wbtalk_search.html', {'wbtalk_list': wbtalk_list})

def pic(request):
    '''
    图片识别
    :param request:
    '''
    pcpt = handlefile.getPath('wbfile/wbtalk_pic/')
    img_list = os.listdir(pcpt)
    neutral, political, terrorism, porn = syh_imgre.imgreco(img_list)
    pic_html = {'neutral': len(neutral), 'politial_len': len(political), 'politial': political,
                'terrorism_len': len(terrorism), 'terrorism': terrorism, 'porn_len': len(porn), 'porn': porn}
    return render(request, 'wbtalk_pic.html', {'pic': pic_html})

def sendtalk(request):
    '''
    发布微博博文
    :param request:
    '''
    if request.method == 'GET':
        return render(request, 'wbtalk_send.html')
    elif request.method == 'POST':
        topic = request.POST.get('topic')
        blog = request.POST.get('blog')
        syh_talk.blog_po(topic, blog)
        return redirect('/wbtalk/show/')

def report_talk(request):
    '''
    投诉微博博文
    :param request:
    '''
    if request.method == 'GET':
        mblog_id = request.GET.get('mblog_id')
        if mblog_id is None:
            mblog_id = 'None'
        return render(request, 'wbtalk_report.html', {'mblog_id': mblog_id})
    elif request.method == 'POST':
        mblog_id = request.POST.get('mblog_id')
        like = request.POST.get('like')
        like = str.split(like, '_')
        syh_report.report(like[0], like[1], mblog_id)
        return redirect('/wbtalk/show/')

def report_pic(request):
    '''
    投诉博文图片
    :param request:
    '''
    if request.method == 'GET':
        mid = request.GET.get('mid')
        like = request.GET.get('like')
        mid = str.split(mid, '_')[0]
        return render(request, 'wbpic_report.html', {'mblog_id': mid, 'like':like})
    elif request.method == 'POST':
        mblog_id = request.POST.get('mblog_id')
        like = request.POST.get('like')
        like = str.split(like, '_')
        syh_report.report(like[0], like[1], mblog_id)
        return redirect('/infosec/test/')

def badword():
    '''
    返回文件中的违规词
    :return: 违规词列表
    '''
    flpt = handlefile.getPath('wbfile/badword/')
    bwlist = ['porn.txt', 'poli.txt', 'terr.txt']
    bw = []
    for i in bwlist:
        tmpt = flpt + i
        bwfl = open(tmpt, 'r', encoding = 'UTF-8')
        for line in bwfl:
            bw.append(line.strip().split(',')[0])
            # strip()用于移除字符串头尾指定的字符
    return bw

'''
def emoju(text):
    emore = SnowNLP(text)
    print(emore.sentiments)
    if emore.sentiments <= 0.35:
        emo = '温和'
    elif emore.sentiments >= 0.75:
        emo = '激进'
    else:
        emo = '中性'
    return emo
'''
