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
    url(r'admin/$', 'admin.views.listing'),    # 首页
    url(r'admin/add/$', 'admin.views.add'),    # 添加问卷
    url(r'admin/list/$', 'admin.views.listing'),    # 问卷列表(问卷管理)
    url(r'admin/edit/(\d+)/$', 'admin.views.edit'),    # 修改问卷
    url(r'admin/delete/(\d+)/$', 'admin.views.delete'),    # 删除问卷
    ## 问题管理
    url(r'admin/(\d+)/add/$', 'admin.views.add_question'),    # 添加问题
    url(r'admin/q(\d+)/edit/$', 'admin.views.edit_question'),    # 修改问题
    url(r'admin/q(\d+)/delete/$', 'admin.views.delete_question'),    # 删除问题
    ## 选项管理
    url(r'admin/q(\d+)/add/', 'admin.views.add_option'),    # 添加选项
    url(r'admin/o(\d+)/add/', 'admin.views.edit_option'),    # 修改选项
    url(r'admin/o(\d+)/delete/', 'admin.views.delete_option'),    # 删除选项
    ## 报表管理
    url(r'admin/(\d+)/report/$', 'admin.views.view_report'),    # 查看报表
    url(r'admin/(\d+)/report/update/$', 'admin.views.update_report'),    # 更新报表


)