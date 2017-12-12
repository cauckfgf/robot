# -*- coding: utf-8 -*-
from django.shortcuts import render,render_to_response
from django.template import loader,Context,RequestContext
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@csrf_exempt
def index_view(request):
    return render_to_response('index.html', RequestContext(request,locals()))
