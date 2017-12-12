# -*- coding: utf-8 -*-
from rest_framework import serializers

from models import *

class DirectorySerializer(serializers.HyperlinkedModelSerializer):
    '''文件夹'''
    id = serializers.ReadOnlyField()
    class Meta:
        model = Directory
        fields = ('id','name','parent','createtime','url')

class DocumentSerializer1(serializers.HyperlinkedModelSerializer):
    '''文件'''
    id = serializers.ReadOnlyField()
    fileurl = serializers.ReadOnlyField()
    class Meta:
        model = Document
        fields = '__all__'

class Doc2RelateSerializer(serializers.HyperlinkedModelSerializer):
    '''文件关联文件夹'''
    id = serializers.ReadOnlyField()
    document = DocumentSerializer1(read_only=True)
    relate = serializers.ReadOnlyField()
    class Meta:
        model = Doc2Relate
        fields = '__all__'

class Doc2RelateSerializer1(serializers.HyperlinkedModelSerializer):
    '''文件关联文件夹'''
    id = serializers.ReadOnlyField()
    relate = serializers.ReadOnlyField()
    class Meta:
        model = Doc2Relate
        fields = '__all__'

class DocumentSerializer(serializers.HyperlinkedModelSerializer):
    '''文件'''
    id = serializers.ReadOnlyField()
    fileurl = serializers.ReadOnlyField()
    Doc2Relates = Doc2RelateSerializer1(many=True,read_only=True)
    class Meta:
        model = Document
        fields = '__all__'