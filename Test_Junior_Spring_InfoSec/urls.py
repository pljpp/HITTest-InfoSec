from django.contrib import admin
from django.urls import path
from wbinfosec.views import infosec_test
from wbinfosec.views import wbtop_view, wbtalk_view, wbuser_view, wbcomment_view

urlpatterns = [
    path('admin/', admin.site.urls),
    # 应用首页
    path('infosec/test/', infosec_test.infosec_test),
    # 微博热搜获取
    path('wbtop/new/', wbtop_view.new),
    # 微博热搜分析
    path('wbtop/show/', wbtop_view.show),
    # 微博话题内容获取
    path('wbtalk/new/', wbtalk_view.new),
    # 微博话题内容分析
    path('wbtalk/show/', wbtalk_view.show),
    # 微博用户信息获取
    path('wbuser/new/', wbuser_view.new),
    # 微博用户信息分析
    path('wbuser/show/', wbuser_view.show),
    # 微博评论获取
    path('wbcomment/new/', wbcomment_view.new),
    # 微博评论分析
    path('wbcomment/show/', wbcomment_view.show),
    # 微博话题内容输入
    path('need/wbtalk/', wbtalk_view.new),
    # 微博用户信息输入
    path('need/wbuser/', wbuser_view.new),
    # 微博评论信息输入
    path('need/wbcomment/', wbcomment_view.new),
    # 微博话题关键词搜索
    path('wbtalk/search/', wbtalk_view.text),
    # 微博话题图片识别
    path('wbtalk/pic/', wbtalk_view.pic),
    # 微博风向引导
    path('wbtalk/sendtalk/', wbtalk_view.sendtalk),
    # 微博博文投诉
    path('wbtalk/report/', wbtalk_view.report_talk),
    # 微博用户投诉
    path('wbuser/report/', wbuser_view.report_user),
    # 微博图片投诉
    path('wbpic/report/', wbtalk_view.report_pic),
]
