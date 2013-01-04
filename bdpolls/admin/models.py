#-*- coding: utf-8 -*-

from django.db import models

class Questionnaire(models.Model):
    """问卷"""

    title = models.CharField(max_length=200, verbose_name=u'问卷标题')
    introduction = models.TextField(blank=True, null=True, verbose_name=u'问卷简介')
    thanking = models.TextField(blank=True, null=True, verbose_name=u'感谢语')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
    updated = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

class Question(models.Model):
    """问题"""

    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    order = models.IntegerField(verbose_name=u'问题序号')
    content = models.TextField(verbose_name=u'问题内容')
    is_multiple_choice = models.BooleanField(default=False, verbose_name=u'是否多选题')

class Option(models.Model):
    """选项(每个问题的各个选项)"""

    question = models.ForeignKey(Question, verbose_name=u'相关问题')
    order = models.IntegerField(verbose_name=u'选项序号')
    content = models.CharField(max_length=200, verbose_name=u'选项内容')

class Report(models.Model):
    """报表"""

    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

class Percentage(models.Model):
    """百分比(每份答卷每个问题每个选项选择的百分比)"""

    report = models.ForeignKey(Report, verbose_name=u'相关报表')
    question = models.ForeignKey(Question, verbose_name=u'相关问题')
    option = models.ForeignKey(Option, verbose_name=u'相关选项')
    amount = models.IntegerField(verbose_name=u'被选择的总次数')
    percent = models.FloatField(verbose_name=u'被选择的百分比')
