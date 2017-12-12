# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
def index_view(request):
    return render_to_response('index.html', RequestContext(request,locals()))
