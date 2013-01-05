#-*- coding: utf-8 -*-

from django import forms
from django.db import models

class Questionnaire(models.Model):
    """问卷表"""

    title = models.CharField(max_length=200, verbose_name=u'问卷标题')
    introduction = models.TextField(blank=True, null=True, verbose_name=u'问卷简介')
    thanking = models.TextField(blank=True, null=True, verbose_name=u'感谢语')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'添加时间')
    updated = models.DateTimeField(auto_now=True, verbose_name=u'修改时间')

    def __unicode__(self):
        return self.title

    def questions(self):
        return self.question_set.order_by('order')

class Question(models.Model):
    """问题表"""

    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    order = models.IntegerField(verbose_name=u'问题序号')
    content = models.TextField(verbose_name=u'问题内容')
    is_multiple_choice = models.BooleanField(default=False, verbose_name=u'是否多选题')

    def __unicode__(self):
        return u'%s的第%d个问题' % (self.questionnaire, self.order)

    def options(self):
        return self.option_set.order_by('order')

class Option(models.Model):
    """选项表(每个问题的各个选项)"""

    question = models.ForeignKey(Question, verbose_name=u'相关问题')
    order = models.IntegerField(verbose_name=u'选项序号')
    content = models.CharField(max_length=200, verbose_name=u'选项内容')
    
    def __unicode__(self):
        return u'第%d个问题的第%d个选项' % (self.question.order, self.order)

    def abc(self):
        """返回用大写字母表示的序号"""

        return chr(ord('A') + self.order - 1)

    def percentage(self):
        """返回百分比(统计报表)"""
        
        report = Report.objects.filter(questionnaire=self.question.questionnaire).order_by('-created')[0]
        percentage = Percentage.objects.get(report=report, option=self)
        return percentage

class Report(models.Model):
    """报表表"""

    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    total = models.IntegerField(verbose_name=u'参与人数')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __unicode__(self):
        return u'%s的统计报表' % self.questionnaire

class Percentage(models.Model):
    """百分比表(每份答卷每个问题每个选项选择的百分比)"""

    report = models.ForeignKey(Report, verbose_name=u'相关报表')
    question = models.ForeignKey(Question, verbose_name=u'相关问题')
    option = models.ForeignKey(Option, verbose_name=u'相关选项')
    amount = models.IntegerField(verbose_name=u'被选择的总次数')
    percent = models.FloatField(verbose_name=u'被选择的百分比')

    def __unicode__(self):
        return u'第%d题的第%d个选项的百分比' % (self.question.order, self.option.order)

class QuestionnaireForm(forms.ModelForm):
    """问卷表单"""

    class Meta:
        model = Questionnaire

class QuestionForm(forms.ModelForm):
    """问题表单"""

    class Meta:
        model = Question
        exclude = ('questionnaire', 'order',)

class OptionForm(forms.ModelForm):
    """选项表单"""

    class Meta:
        model = Option
        exclude = ('question', 'order',)
