# -*- coding: utf-8 -*-
from django.db import models

class Action(models.Model):
    '''业务api'''
    url = models.CharField(max_length=128,verbose_name=u'业务url')

class Keyword(models.Model):
    '''关键字'''
    content = models.CharField(max_length=128,verbose_name=u'应答内容')
    action = models.ForeignKey(Action,verbose_name='动作对应api',blank=True,null=True)

class Answer(models.Model):
    content = models.CharField(max_length=128,verbose_name=u'应答内容')
    keyword = models.ForeignKey(Keyword,verbose_name=u'应答内容关键字',blank=True,null=True)

class Question(models.Model):
    '''机器人库'''
    content = models.CharField(max_length=128,verbose_name=u'问题内容')
    answer = models.ForeignKey(Answer,verbose_name='应答',blank=True,null=True)
    def synPY(self):
        '''同步拼音'''
        self.pinyin = p.get_pinyin(self.standard)
        self.save()



