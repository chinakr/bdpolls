#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib import messages
from admin.models import Questionnaire
from admin.models import QuestionnaireForm

def listing(request):
    """问卷列表(问卷管理)"""

    questionnaires = Questionnaire.objects.order_by('-created')

    return render(request, 'admin/list.html', {
        'questionnaires': questionnaires,
    })

def add(request):
    """添加问卷"""

    if request.method == 'POST':
        form = QuestionnaireForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, u'调查问卷`%s`添加成功。' % request.POST['title'])
            return redirect('/admin/list/')
    else:
        form = QuestionnaireForm()

    return render(request, 'admin/add.html', {
        'form': form,
    })

def edit(request, questionnaire_id):
    """修改问卷"""

    pass

def delete(request, questionnaire_id):
    """删除问卷"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    title = questionnaire.title
    questionnaire.delete()
    messages.success(request, u'调查问卷`%s`已删除。' % title)

    return redirect('/admin/list/')

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
