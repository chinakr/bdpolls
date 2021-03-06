#-*- coding: utf-8 -*-

from django import forms
from django.db import models
from django.contrib.auth.models import User
from admin.models import Questionnaire, Question, Option

class UserProfile(models.Model):
    """自定义用户信息"""

    user = models.OneToOneField(User)
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'姓名')
    mobile = models.CharField(max_length=50, blank=True, null=True, verbose_name=u'手机')

    def __unicode__(self):
        return self.name

    def last_visit(self):
        """最后到访时间(参与调查问卷的时间)"""

        try:
            feedback = self.user.feedback_set.order_by('-created')[0]
            return feedback.created
        except:
            print 'DEBUG: last_visit - feedback error - %s' % self
            return ''

    def last_feedback(self):
        """最后参与的调查问卷"""

        try:
            feedback = self.user.feedback_set.order_by('-created')[0]
            return feedback
        except:
            print 'DEBUG: last_feedback - feedback error - %s' % self
            return ''

class Feedback(models.Model):
    """答卷(反馈)"""

    questionnaire = models.ForeignKey(Questionnaire, verbose_name=u'相关问卷')
    user = models.ForeignKey(User, verbose_name=u'相关用户')
    message = models.TextField(blank=True, null=True, verbose_name=u'留言')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'提交时间')

    def __unicode__(self):
        return u'%s的答卷' % self.questionnaire

class Answer(models.Model):
    """答案(每份答卷每个问题的答案)"""

    feedback = models.ForeignKey(Feedback, verbose_name=u'相关答卷')
    question = models.ForeignKey(Question, verbose_name=u'相关问题')
    option = models.ForeignKey(Option, verbose_name=u'相关选项')

    def __unicode__(self):
        return u'%s的第%d个问题的选项%s' % (self.feedback, self.question.order, self.option.abc)

class UserForm(forms.ModelForm):
    """用户表单"""

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
