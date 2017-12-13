# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from .serializers import *
# import Levenshtein
import json

from .models import *


class KeywordSet(viewsets.ModelViewSet):
    queryset = Keyword.objects.all()
    serializer_class = KeywordSerializer

class AnswerSet(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class QuestionSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

from .seq2seq import seq2seq
@csrf_exempt
def AnswerMe(request):
    qustion = request.GET.get('qustion',None)
    if qustion:
        seq = seq2seq()
        answer = seq.answer(qustion)
        return HttpResponse(json.dumps({'answer':answer}), content_type="application/json" )
    else:
        return HttpResponse(json.dumps({'answer':'请提问'}), content_type="application/json" )

@csrf_exempt
def Train(request):
    if request.method == 'POST':
        action = request.POST.get('action',None)
        seq = seq2seq()
        if action=='train':
            input_strs = request.POST.get('input_strs',None)
            target_strs = request.POST.get('target_strs',None)
            seq.onlinelearning(input_strs,target_strs)
        elif action=='retrain':
            seq.preprocess()
            seq.clearModel(0)
            seq.train()
        return HttpResponse(json.dumps({'over':'succ'}), content_type="application/json" )

