# @PydevCodeAnalysisIgnore
from django.shortcuts import render, redirect
from wbinfosec.utils import wbcomment_util, wmmatch, wbapi

def new(request):
    '''
    展示微博搜索内容
    :param request:
    '''
    if request.method == 'GET':
        need_id = request.GET.get('need_id')
        if need_id is None:
            return render(request, 'infosec_need.html')
    elif request.method == 'POST':
        need_id = request.POST.get('need_id')
    wbcomment_util.makehtml(need_id)
    wbcomment_list = wbcomment_util.showfile()
    return render(request, 'wbcomment_new.html', {'wbcomment_list': wbcomment_list})

def show(request):
    '''
    评论引导舆论风向
    '''
    if request.method == 'GET':
        return render(request, 'wbcomment_show.html')
    elif request.method == 'POST':
        api_comment = request.POST.get('api_comment')
        api_mblogid = request.POST.get('api_mblogid')
        print('comment: ', api_comment)
        print('mblogid: ', api_mblogid)
        if api_comment is None or api_comment == '' or api_mblogid is None or api_mblogid == '':
            return render(request, 'wbcomment_show.html')
        api_info = wbapi.comment_api(api_comment, api_mblogid)
        if api_info is None:
            return render(request, 'wbcomment_show.html')
        else:
            return redirect('/infosec/test/')
