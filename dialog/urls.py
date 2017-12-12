# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import *

from rest_framework import routers
router = routers.DefaultRouter()
router.register(r'action', ActionSet)
router.register(r'keywork', KeywordSet)
router.register(r'answer', AnswerSet)
router.register(r'question', QuestionSet)
urlpatterns = [
    url(r'^answerme/', AnswerMe),
    url(r'^train/', Train),
    #restframe
    url(r'^rest/', include(router.urls)),

]
