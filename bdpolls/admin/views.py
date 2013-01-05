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

    from_url = request.META['HTTP_REFERER']
    question = Question.objects.get(pk=question_id)
    from_url += '#q%d' % question.order
    if request.method == 'POST':
        from_url = request.POST['from_url']
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, u'%s修改成功。' % question)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'admin/edit_question.html', {
        'question': question,
        'form': form,
        'from_url': from_url,
    })

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

def move_question(request, question_id, action):
    """移动问题(改变序号)"""

    from_url = request.META['HTTP_REFERER']
    question = Question.objects.get(pk=question_id)
    if action == 'up' and question.order != 1:
        related_question = Question.objects.get(questionnaire=question.questionnaire, order=question.order-1)
        related_question.order += 1
        related_question.save()
        question.order -= 1
        question.save()
    elif action == 'down' and question.order != question.questionnaire.question_set.count():
        related_question = Question.objects.get(questionnaire=question.questionnaire, order=question.order+1)
        related_question.order -= 1
        related_question.save()
        question.order += 1
        question.save()
    
    from_url += '#q%d' % question.order
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

    from_url = request.META['HTTP_REFERER']
    option = Option.objects.get(pk=option_id)
    from_url += '#q%d' % option.question.order
    if request.method == 'POST':
        from_url = request.POST['from_url']
        form = OptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            messages.success(request, u'%s修改成功。' % option)
    else:
        form = OptionForm(instance=option)

    return render(request, 'admin/edit_option.html', {
        'option': option,
        'form': form,
        'from_url': from_url,
    })

def delete_option(request, option_id):
    """删除选项"""

    from_url = request.META['HTTP_REFERER']

    option = Option.objects.get(pk=option_id)
    question = option.question
    order = option.order
    option.delete()
    options = Option.objects.filter(order__gt=order)
    for option in options:
        option.order -= 1
        option.save()
    
    from_url += '#q%d' % question.id
    return redirect(from_url)

def move_option(request, option_id, action):
    """移动选项(改变序号)"""

    pass

def view_report(request, report_id):
    """查看报表"""

    pass

def update_report(request, report_id):
    """更新报表"""

    pass
