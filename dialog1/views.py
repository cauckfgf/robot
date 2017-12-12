# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required

# import Levenshtein
import json

from .models import *

# import gensim.models.word2vec as w2v
# m = w2v.Word2Vec.load("space_model.txt")
# Create your views here.

from .dialog import *

@csrf_exempt
@login_required(login_url="/login/") 
def similar(request):
    s = request.GET.get('s')
    ctype = request.GET.get('ctype')
    sim = Similar()
    sim.option(s,ctype)
    rdata = sim.getmostsimllar()
    return HttpResponse(json.dumps(rdata), content_type="application/json" )

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View
from lxml import etree
from django.utils.encoding import smart_str
import hashlib
import time
from django.template.loader import render_to_string
from django.views.decorators.csrf import ensure_csrf_cookie

@csrf_exempt
def wx(request):
    if request.method == 'GET':
        #下面这四个参数是在接入时，微信的服务器发送过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)

        #这里的token需要自己设定，主要是和微信的服务器完成验证使用
        token = 'fgf1987'

        #把token，timestamp, nonce放在一个序列中，并且按字符排序
        hashlist = [token, timestamp, nonce]
        hashlist.sort()

        #将上面的序列合成一个字符串
        hashstr = ''.join([s for s in hashlist])

        #通过python标准库中的sha1加密算法，处理上面的字符串，形成新的字符串。
        hashstr = hashlib.sha1(hashstr.encode(encoding='utf-8')).hexdigest()

        #把我们生成的字符串和微信服务器发送过来的字符串比较，
        #如果相同，就把服务器发过来的echostr字符串返回去
        if hashstr == signature:
          return HttpResponse(echostr)

    if request.method == 'POST':
        #将程序中字符输出到非 Unicode 环境（比如 HTTP 协议数据）时可以使用 smart_str 方法
        data = smart_str(request.body)
        #将接收到数据字符串转成xml
        xml = etree.fromstring(data)

        #从xml中读取我们需要的数据。注意这里使用了from接收的to，使用to接收了from，
        #这是因为一会我们还要用这些数据来返回消息，这样一会使用看起来更符合逻辑关系
        fromUser = xml.find('ToUserName').text
        toUser = xml.find('FromUserName').text
        msg_type = xml.find('MsgType').text
        Content = xml.find('Content').text
        #这里获取当前时间的秒数，time.time()取得的数字是浮点数，所以有了下面的操作
        nowtime = str(int(time.time()))
        tl = Tuling()
        # return HttpResponse()
        #加载text.xml模板,参见render()调用render_to_string()并将结果馈送到 HttpResponse适合从视图返回的快捷方式 。
        if msg_type == 'text':
            res = tl.v1(Content)
            # res2 = tl.v2(Content)
            
            if res['code']==100000:
                replyMsg = AllMsg(toUser, fromUser, res['text'])
                print replyMsg.Txt()
                return HttpResponse(replyMsg.Txt())
            elif res['code']==200000:
                # replyMsg = AllMsg(toUser, fromUser, res['text'],picurl=res['url'])
                # print replyMsg.ImgTxt()
                # return HttpResponse(replyMsg.ImgTxt())
                txt = "%s<a href='%s'>打开页面</a>"%(res['text'],res['url'])
                replyMsg = AllMsg(toUser, fromUser, txt)
                print replyMsg.Txt()
                return HttpResponse(replyMsg.Txt())

        elif msg_type == 'image':
            content = "图片已收到,谢谢"
            replyMsg = AllMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.Txt())
        elif msg_type == 'voice':
            content = "语音已收到,谢谢"
            replyMsg = AllMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.Txt())
        elif msg_type == 'video':
            content = "视频已收到,谢谢"
            replyMsg = AllMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.Txt())
        elif msg_type == 'shortvideo':
            content = "小视频已收到,谢谢"
            replyMsg = AllMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.Txt())
        elif msg_type == 'location':
            content = "位置已收到,谢谢"
            replyMsg = AllMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.Txt())
        else:
            msg_type == 'link'
            content = "链接已收到,谢谢"
            replyMsg = AllMsg(toUser, fromUser, content)
            return HttpResponse(replyMsg.Txt())




# class Msg(object):
#     def __init__(self, xmlData):
#         self.ToUserName = xmlData.find('ToUserName').text
#         self.FromUserName = xmlData.find('FromUserName').text
#         self.CreateTime = xmlData.find('CreateTime').text
#         self.MsgType = xmlData.find('MsgType').text
#         self.MsgId = xmlData.find('MsgId').text

import time
class AllMsg(object):
    def __init__(self, toUserName, fromUserName, content,picurl='',url=''):
        self.__dict = dict()
        self.__dict['ToUserName'] = toUserName
        self.__dict['FromUserName'] = fromUserName
        self.__dict['CreateTime'] = int(time.time())
        self.__dict['Content'] = content
        self.__dict['picurl'] = picurl
        self.__dict['url'] = url

    def Txt(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**self.__dict)

    def ImgTxt(self):
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[news]]></MsgType>
        <ArticleCount>1</ArticleCount>
        <Articles>
        <item>
        <Title><![CDATA[{Content}]]></Title> 
        <Description><![CDATA[]]></Description>
        <PicUrl><![CDATA[{picurl}]]></PicUrl>
        <Url><![CDATA[{picurl}]]></Url>
        </item>
        </Articles>
        </xml>
        """
        return XmlForm.format(**self.__dict)



@csrf_exempt
@login_required(login_url="/login/") 
def dialog(request):
    stm = None
    sdb = None
    if StateMachineDB.objects.filter(user_id=request.user.id).count():
        sdb = StateMachineDB.objects.get(user_id=request.user.id)
        stm = sdb.stm()
    else:
        stm = DialogMachine()
        sdb = StateMachineDB.objects.create(user_id=request.user.id)
        sdb.pksave(stm)
    m = request.GET.get('m')
    rdata = {}
    if m:
        most = stm.to(m)
        rdata = {'hide':most}
    else:
        stm.current_state = stm.start
    sdb.pksave(stm)
    
    if stm.again:
        rdata['show'] = [u'没有听清楚,请再说一次']
    else:
        if stm.is_start:
            rdata['show'] = [u'发起维修单',u'页面导航',u'随便聊聊']
        elif stm.is_space:
            rdata['show'] = [u'那里坏了',u'如:儿科大楼4层401房间',u'返回']
        elif stm.is_device:
            rdata['show'] = [u'什么坏了',u'如:空调',u'返回']
        elif stm.is_submit:
            rdata['show'] = [u'提交确认',u'如:好的',u'返回']
        elif stm.is_html:
            rdata['show'] = [u'首页',u'文件管理',u'维修单列表',u'维保单列表',u'发起维修单',u'处理问题',u'浏览模型',u'维修总览',u'退出']

        elif stm.is_tuling:
            try:
                rdata['show'] = [rdata['hide']['obj']['text']]
            except:
                rdata['show'] =[u'你想聊什么?']
    return HttpResponse(json.dumps(rdata), content_type="application/json" )

# import platform.system()
# if platform.system()=='Windows':
#     from .tf.tf import robot
#     def tensorflow(request):
#         i = request.GET.get('input',None)
#         o = request.GET.get('output',None)
#         action = request.GET.get('action',None)
#         if action == 'train':
#             robot.tf(i,o)
#         else:
#             robot.out(i)
#         return HttpResponse("{'res':'succ'}", content_type="application/json" )