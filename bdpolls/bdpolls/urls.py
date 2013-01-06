#-*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bdpolls.views.home', name='home'),
    # url(r'^bdpolls/', include('bdpolls.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # 管理后台
    ## 问卷管理
    url(r'^admin/$', 'admin.views.listing'),    # 首页
    url(r'^admin/add/$', 'admin.views.add'),    # 添加问卷
    url(r'^admin/list/$', 'admin.views.listing'),    # 问卷列表(问卷管理)
    url(r'^admin/edit/(\d+)/$', 'admin.views.edit'),    # 修改问卷(问题管理)
    url(r'^admin/delete/(\d+)/$', 'admin.views.delete'),    # 删除问卷
    ## 问题管理
    url(r'^admin/(\d+)/add/$', 'admin.views.add_question'),    # 添加问题
    url(r'^admin/q(\d+)/edit/$', 'admin.views.edit_question'),    # 修改问题
    url(r'^admin/q(\d+)/delete/$', 'admin.views.delete_question'),    # 删除问题
    url(r'^admin/q(\d+)/(up|down)/$', 'admin.views.move_question'),    # 移动问题(改变序号)
    ## 选项管理
    url(r'^admin/q(\d+)/add/', 'admin.views.add_option'),    # 添加选项
    url(r'^admin/o(\d+)/edit/', 'admin.views.edit_option'),    # 修改选项
    url(r'^admin/o(\d+)/delete/', 'admin.views.delete_option'),    # 删除选项
    url(r'^admin/o(\d+)/(up|down)/$', 'admin.views.move_option'),    # 移动选项(改变序号)
    ## 报表管理
    url(r'^admin/(\d+)/report/$', 'admin.views.view_report'),    # 查看报表
    url(r'^admin/(\d+)/report/update/$', 'admin.views.update_report'),    # 更新报表
    ## 用户管理
    url(r'^admin/user/(system|common)/$', 'admin.views.list_user'),    # 用户列表；system - 系统用户(后台用户)，common - 普通用户(前台用户)
    url(r'^admin/user/add/$', 'admin.views.add_user'),    # 添加系统用户
    url(r'^admin/user/(\d+)/$', 'admin.views.view_user'),    # 查看用户
    url(r'^admin/user/(\d+)/edit/$', 'admin.views.edit_user'),    # 修改用户
    url(r'^admin/user/(\d+)/delete/$', 'admin.views.delete_user'),    # 删除用户

    # 前台
    url(r'^$', 'survey.views.listing'),    # 首页
    url(r'^list/$', 'survey.views.listing'),    # 问卷列表
    url(r'^(\d+)/$', 'survey.views.join'),    # 填写问卷
    url(r'^(\d+)/thanks/$', 'survey.views.thanks'),    # 感谢(广告)

    # 用户登录
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),    # 用户登录
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),    # 用户退出
)
