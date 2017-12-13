# -*- coding: utf-8 -*-
from django.db import models

class Keyword(models.Model):
    '''关键字'''
    content = models.CharField(max_length=128,verbose_name=u'应答内容')
    remark = models.CharField(max_length=128,verbose_name=u'备注')
    action = models.CharField(max_length=128,verbose_name=u'业务url')
    actiontype = models.CharField(max_length=128,verbose_name=u'url调用类型:get,put,post,delete')

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



