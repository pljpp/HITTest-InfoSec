# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from wbinfosec.utils import wbuser_util, wmmatch, syh_report
from wbinfosec.views.wbtalk_view import badword

def new(request):
    '''
    爬取用户主页并展示
    :param request: 
    '''
    if request.method == 'GET':
        need_id = request.GET.get('need_id')
        if need_id is None:
            return render(request, 'infosec_need.html')
        else:
            need_num = 20
    elif request.method == 'POST':
        need_id = request.POST.get('need_id')
        need_num = request.POST.get('need_num')
        if int(need_num) <= 0 or need_id is None or need_num is None or need_id == '' or need_num == '':
            return render(request, 'infosec_need.html')
    wbuser_util.makehtml(need_id, need_num)
    list_wbuser = wbuser_util.showfile()
    wbuser_info = list_wbuser[0]
    list_wbuser = list_wbuser[1:]
    return render(request, 'wbuser_new.html', {'wbuser_info': wbuser_info, 'list_wbuser': list_wbuser})

def show(request):
    '''
    展示用户主页
    :param request: 
    '''
    if request.method == 'GET':
        list_wbuser = wbuser_util.showfile()
        wbuser_info = list_wbuser[0]
        list_wbuser = list_wbuser[1:]
        mode = badword()
        wm = wmmatch.DHSWM(mode)
        for wbuser_for in list_wbuser:
            mate = []
            wmresult = wm.search(wbuser_for['text'])
            for forwm in wmresult:
                if len(wmresult[forwm]) > 0:
                    mate.append((forwm, len(wmresult[forwm])))
            if mate == []:
                mate = ['None']
            wbuser_for['mate'] = mate
        # 列表是有序序列, 可以通过比对列表标号获得博文的id
        return render(request, 'wbuser_show.html', {'wbuser_info': wbuser_info, 'list_wbuser': list_wbuser})

def report_user(request):
    '''
    投诉微博博文
    :param request:
    '''
    if request.method == 'GET':
        mblog_id = request.GET.get('mid')
        print('>>>>mblog_id=', mblog_id)
        if mblog_id is None:
            mblog_id = 'None'
        return render(request, 'wbtalk_report.html', {'mblog_id': mblog_id})
    elif request.method == 'POST':
        mblog_id = request.POST.get('mblog_id')
        like = request.POST.get('like')
        like = str.split(like, '_')
        syh_report.report(like[0], like[1], mblog_id)
        return redirect('/wbuser/show/')