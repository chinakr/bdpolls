#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from admin.models import Questionnaire, Question, Option

class Feedback(models.Model):
    """答卷(反馈)"""

    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    user = models.ForeignKey(User, verbose_name=u'相关用户')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'提交时间')

class Answer(models.Model):
    """答案(每份答卷每个问题的答案)"""

    feedback = models.ForeignKey(Feedback, verbose_name=u'相关答卷')
    question = models.ForeignKey(Question, verbose_name=u'相关问题')
    option = models.ForeignKey(Option, verbose_name=u'相关选项')
