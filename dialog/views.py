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

class ActionSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer

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
        if action=='train':
            seq.train()
        elif action=='retrain':
            seq.clearModel(0)
            seq.train()

