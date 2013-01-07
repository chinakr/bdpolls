#-*- coding: utf-8 -*-

from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from admin.models import Questionnaire, Question, Option, Report, Percentage
from admin.models import QuestionnaireForm, QuestionForm, OptionForm
from survey.models import Feedback, Answer, UserProfile
from survey.models import UserForm

@login_required
def listing(request):
    """问卷列表(问卷管理)"""

    questionnaires = Questionnaire.objects.order_by('-created')

    return render(request, 'admin/list.html', {
        'questionnaires': questionnaires,
    })

@login_required
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

@login_required
def edit(request, questionnaire_id):
    """修改问卷(问题管理)"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    return render(request, 'admin/edit.html', {
        'questionnaire': questionnaire,
    })

@login_required
def modify(request, questionnaire_id):
    """修改问卷(标题等)"""

    from_url = request.META['HTTP_REFERER']
    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    if request.method == 'POST':
        from_url = request.POST['from_url']
        form = QuestionnaireForm(request.POST, instance=questionnaire)
        if form.is_valid():
            form.save()
            messages.success(request, u'%s保存成功。' % questionnaire)
    else:
        form = QuestionnaireForm(instance=questionnaire)

    return render(request, 'admin/modify.html', {
        'form': form,
        'from_url': from_url,
    })

@login_required
def delete(request, questionnaire_id):
    """删除问卷"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    title = questionnaire.title
    questionnaire.delete()
    messages.success(request, u'调查问卷`%s`已删除。' % title)

    return redirect('/admin/list/')

@login_required
def reorder(request, questionnaire_id):
    """给所有问题的所有选项重新排序(解决选项序号重复问题)"""

    from_url = request.META['HTTP_REFERER']
    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    for question in questionnaire.questions():
        count = 0
        for option in question.options():
            count += 1
            option.order = count
            option.save()

    return redirect(from_url)

@login_required
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

@login_required
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

@login_required
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

@login_required
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

@login_required
def reorder_options(request, question_id):
    """给问题选项重新排序(解决选项序号重复的问题)"""

    from_url = request.META['HTTP_REFERER']
    question = Question.objects.get(pk=question_id)

    count = 0
    for option in question.options():
        count += 1
        option.order = count
        option.save()

    from_url += '#q%d' % question.order
    return redirect(from_url)

@login_required
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

@login_required
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

@login_required
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

@login_required
def move_option(request, option_id, action):
    """移动选项(改变序号)"""

    from_url = request.META['HTTP_REFERER']
    option = Option.objects.get(pk=option_id)
    from_url += '#q%d' % option.question.order
    if action == 'up' and option.order != 1:
        related_option = Option.objects.get(question=option.question, order=option.order-1)
        related_option.order += 1
        related_option.save()
        option.order -= 1
        option.save()
    elif action == 'down' and option.order != option.question.option_set.count():
        related_option = Option.objects.get(question=option.question, order=option.order+1)
        related_option.order -= 1
        related_option.save()
        option.order += 1
        option.save()
    
    return redirect(from_url)

@login_required
def view_report(request, questionnaire_id):
    """查看报表"""
   
    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    if Report.objects.filter(questionnaire=questionnaire).exists():    # 显示最新Report
        report = Report.objects.filter(questionnaire=questionnaire).order_by('-created')[0]
    else:    # 新建并显示Report
        total = Feedback.objects.filter(questionnaire=questionnaire).count()
        report = Report.objects.create(questionnaire=questionnaire, total=total)
        for question in questionnaire.questions():
            for option in question.options():
                amount = Answer.objects.filter(question=question, option=option).count()
                percent = 1.0 * amount / report.total * 100
                Percentage.objects.create(report=report, question=question, option=option, amount=amount, percent=percent)

    return render(request, 'admin/report.html', {
        'report': report,
    })

@login_required
def update_report(request, questionnaire_id):
    """更新报表"""

    from_url = request.META['HTTP_REFERER']
    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)
    report = Report.objects.filter(questionnaire=questionnaire).order_by('-created')[0]
    total = Feedback.objects.filter(questionnaire=questionnaire).count()
    if report.total < total:
        report = Report.objects.create(questionnaire=questionnaire, total=total)    # 更新Report
        for question in questionnaire.questions():    # 更新Percentage
            for option in question.options():
                amount = Answer.objects.filter(question=question, option=option).count()
                percent = 1.0 * amount / report.total * 100
                Percentage.objects.create(report=report, question=question, option=option, amount=amount, percent=percent)

    return redirect(from_url)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def list_user(request, user_type, page_num='1'):
    """用户列表

    system - 系统用户(后台用户)
    common - 普通用户(前台用户)
    """

    ITEMS_PER_PAGE = 10

    if user_type == 'system':
        users = User.objects.exclude(username__startswith='auto_user_').order_by('username')
        return render(request, 'admin/system_user.html', {
            'users': users,
        })
    elif user_type == 'common':
        users = UserProfile.objects.filter(user__username__startswith='auto_user_').order_by('-user__date_joined')
        p = Paginator(users, ITEMS_PER_PAGE)
        users = p.page(page_num)
        return render(request, 'admin/common_user.html', {
            'users': users,
        })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_user(request):
    """添加系统用户"""

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/admin/user/system/')
    else:
        form = UserForm()

    return render(request, 'admin/add_user.html', {
        'form': form,
    })

@login_required
def view_user(request, user_id):
    """查看用户"""

    pass

@login_required
@user_passes_test(lambda u: u.is_superuser)
def edit_user(request, user_id):
    """修改用户"""

    from_url = request.META['HTTP_REFERER']
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        from_url = request.POST['from_url']
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, u'用户%s的信息已保存。' % user)
    else:
        form = UserForm(instance=user)

    return render(request, 'admin/edit_user.html', {
        'form': form,
        'from_url': from_url,
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    """删除用户"""

    from_url = request.META['HTTP_REFERER']
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect(from_url)
