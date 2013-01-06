#-*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from admin.models import Questionnaire, Question, Option
from survey.models import UserProfile, Feedback, Answer

def listing(request):
    """问卷列表"""

    questionnaires = Questionnaire.objects.order_by('-updated')

    return render(request, 'survey/list.html', {
        'questionnaires': questionnaires,
    })

def join(request, questionnaire_id):
    """填写问卷"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    if request.method == 'POST':
        name = request.POST['name']    # 姓名
        mobile = request.POST['mobile']    # 手机
        message = request.POST['message']    # 留言
        #print 'DEBUG: name: %s; mobile: %s' % (name, mobile)
        print 'DEBUG: message is `%s`.' % message
        if UserProfile.objects.filter(name=name, mobile=mobile).exists():
            profile = UserProfile.objects.get(name=name, mobile=mobile)
            user = profile.user
        else:
            import random
            username = 'auto_user_%d' % random.randint(100000, 999999)
            user = User.objects.create(username=username, password='helloworld')
            UserProfile.objects.create(user=user, name=name, mobile=mobile)
        feedback = Feedback.objects.create(questionnaire=questionnaire, user=user, message=message)
        for question in questionnaire.questions():
            try:    # 跳过未选择的题
                request.POST['question_%d' % question.id]
            except:
                continue
            if question.is_multiple_choice:
                option_ids = request.POST.getlist('question_%d' % question.id)
                for option_id in option_ids:
                    #print 'DEBUG: option id is %s (*)' % option_id
                    option = Option.objects.get(pk=option_id)
                    Answer.objects.create(feedback=feedback, question=question, option=option)
            else:
                option_id = request.POST['question_%d' % question.id]
                #print 'DEBUG: option id is %s' % option_id
                option = Option.objects.get(pk=option_id)
                Answer.objects.create(feedback=feedback, question=question, option=option)
        return redirect('/%d/thanks/' % questionnaire.id)
            

    return render(request, 'survey/join.html', {
        'questionnaire': questionnaire,
    })

def thanks(request, questionnaire_id):
    """感谢(广告)"""

    questionnaire = Questionnaire.objects.get(pk=questionnaire_id)

    return render(request, 'survey/thanks.html', {
        'questionnaire': questionnaire,
    })
