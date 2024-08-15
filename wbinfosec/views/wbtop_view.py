# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from wbinfosec.utils import wbtop_util

def new(request):
    '''
    爬取微博热搜并展示
    :param request: 
    '''
    wbtop_util.makehtml()
    list_wbtop = wbtop_util.showfile()
    return render(request, 'wbtop_new.html', {'list_wbtop': list_wbtop})

def show(request):
    '''
    展示微博热搜榜单的分析结果
    :param request:
    '''
    wbtop_list = wbtop_util.showfile()
    # 生成柱状图
    htmlbar = bar_wbtop(wbtop_list)
    # 生成扇形图
    htmlpie = pie_wbtop(wbtop_list)
    # 生成词云图
    htmlcloud = cloud_wbtop(wbtop_list)
    return render(request, 'wbtop_show.html', {'htmlbar': htmlbar, 'htmlpie': htmlpie, 'htmlcloud': htmlcloud})

def bar_wbtop(wbtop_list):
    '''
    微博热搜榜单种类柱状图
    :param wbtop_list: 微博热搜榜单内容
    '''
    hotnum = {}
    for forwbtop in wbtop_list:
        category = forwbtop['category'].split(',')[0]
        if category in hotnum:
            hotnum[category] = hotnum[category] + forwbtop['num'] / 10000
        else:
            hotnum.setdefault(category, forwbtop['num'] / 10000)
    htmlbar = wbtop_util.bar(hotnum)
    return htmlbar

def pie_wbtop(wbtop_list):
    '''
    微博热搜榜单种类扇形图
    :param wbtop_list: 微博热搜榜单内容
    '''
    temp = {}
    for forwbtop in wbtop_list:
        category = forwbtop['category'].split(',')[0]
        if category in temp:
            temp[category] = temp[category] + forwbtop['num']
        else:
            temp.setdefault(category, forwbtop['num'])
    hotnum = {}
    hotnum['其他'] = 0
    for fortemp in temp:
        if temp[fortemp] < 1000000:
            hotnum['其他'] = hotnum['其他'] + temp[fortemp]
        else:
            hotnum[fortemp] = temp[fortemp]
    htmlpie = wbtop_util.pie(hotnum)
    return htmlpie

def cloud_wbtop(wbtop_list):
    '''
    微博热搜榜单内容词云图
    :param wbtop_list: 微博热搜榜单内容
    '''
    word = []
    for top in wbtop_list:
        word.append(top['word'])
    htmlcloud = wbtop_util.cloud(word)
    return htmlcloud
