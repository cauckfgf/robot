# -*- coding: utf-8 -*-
from rest_framework import serializers
from .models import *



class KeywordSerializer(serializers.HyperlinkedModelSerializer):
    '''机电系统类型'''
    id = serializers.ReadOnlyField()
    class Meta:
        model = Keyword
        fields = '__all__'

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    '''机电系统类型'''
    id = serializers.ReadOnlyField()
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    '''机电系统类型'''
    id = serializers.ReadOnlyField()
    answer = AnswerSerializer()
    class Meta:
        model = Question
        fields = '__all__'

