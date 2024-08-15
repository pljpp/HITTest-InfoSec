from django.shortcuts import render, redirect

def infosec_test(request):
    '''
    微博内容识别与管控系统首页
    :param request:
    '''
    return render(request, 'infosec_test.html')
