# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from views import *


urlpatterns = [

    url(r'^similar/$', similar),
    url(r'^wx/$', wx),
    url(r'^dialog/$', dialog),
]
# import platform
# if platform.system()=='Windows':
#     urlpatterns += [
#         url(r'^tensorflow/$', tensorflow),
#     ]