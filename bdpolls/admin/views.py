#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib import messages
from admin.models import Questionnaire, Question, Option
from admin.models import QuestionnaireForm, QuestionForm, OptionForm

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
    """修改问卷(问题管理)"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    return render(request, 'admin/edit.html', {
        'questionnaire': questionnaire,
    })

def delete(request, questionnaire_id):
    """删除问卷"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    title = questionnaire.title
    questionnaire.delete()
    messages.success(request, u'调查问卷`%s`已删除。' % title)

    return redirect('/admin/list/')

def add_question(request, questionnaire_id):
    """添加问题"""

    from_url = request.META['HTTP_REFERER']

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    if request.method == 'POST':
        from_url = request.POST['from_url']
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.questionnaire = questionnaire
            question.order = questionnaire.question_set.count() + 1
            question.save()
            messages.success(request, u'第%d个问题已添加。' % question.order)
            return redirect(from_url)
    else:
        form = QuestionForm()

    return render(request, 'admin/add_question.html', {
        'questionnaire': questionnaire,
        'form': form,
        'from_url': from_url,
    })

def edit_question(request, question_id):
    """修改问题"""

    pass

def delete_question(request, question_id):
    """删除问题"""

    from_url = request.META['HTTP_REFERER']

    question = Question.objects.get(pk=question_id)
    name = question
    order = question.order
    question.delete()
    questions = Question.objects.filter(order__gt=order)
    for question in questions:
        question.order -= 1
        question.save()
    messages.success(request, u'第%d个问题已删除。' % order)
    
    return redirect(from_url)

def add_option(request, question_id):
    """添加选项"""

    from_url = request.META['HTTP_REFERER']
    question = Question.objects.get(pk=question_id)
    from_url += '#q%d' % question.order

    if request.method == 'POST':
        from_url = request.POST['from_url']
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question
            option.order = question.option_set.count() + 1
            option.save()
            return redirect(from_url)
    else:
        form = OptionForm()

    return render(request, 'admin/add_option.html', {
        'question': question,
        'form': form,
        'from_url': from_url,
    })

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
