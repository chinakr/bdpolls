#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect

def listing(request):
    """问卷列表(问卷管理)"""

    pass

def add(request):
    """添加问卷"""

    pass

def edit(request, questionnaire_id):
    """修改问卷"""

    pass

def delete(request, questionnaire_id):
    """删除问卷"""

    pass

def add_question(request):
    """添加问题"""

    pass

def edit_question(request, question_id):
    """修改问题"""

    pass

def delete_question(request, question_id):
    """删除问题"""

    pass

def add_option(request):
    """添加选项"""

    pass

def edit_option(request, option_id):
    """修改选项"""

    pass

def delete_option(request, option_id):
    """删除选项"""

    pass

def view_report(request, report_id):
    """查看报表"""

    pass

def update_report(request, report_id):
    """更新报表"""

    pass
