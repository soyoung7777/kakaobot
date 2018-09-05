from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os.path
import sys
import random
import urllib.request
import urllib.parse
import re
import time
from operator import eq
from random import *

from . import pathPrint
from . import anotherPathPrint
from . import SubwayInfo
from . import BusInfo
from . import ExpressInfo

#DB(models.py에서 정의)
from chat.models import allData

try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

#CLIENT_ACCESS_TOKEN = 'f087d3e9915f48e9935bba49078b7d83'
CLIENT_ACCESS_TOKEN = '33615c11c39546908fd8ab5b32dfac16'


def dialogflow(msg_str, session_id):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    dialogflow_request = ai.text_request()

    dialogflow_request.lang = 'ko'
    dialogflow_request.session_id = session_id
    dialogflow_request.query = msg_str
    response = dialogflow_request.getresponse()

    data = json.loads(response.read().decode('utf-8'))
    return data

def keyboard(request):
	return JsonResponse({
		'type' : 'text'
	})

@csrf_exempt
def message(request):
    message = ((request.body).decode('utf-8'))
    msg = json.loads(message)
    user_id = msg['user_key']
    msg_str = msg['content']

    num = alltData.objects.filter(session_id=user_id).count()

	# jsontmp = "22222"
	# dialogflow = 2
    txt = ""

    if num == 0: # 처음
        alltData(session_id=user_id).save()
    #else:

    res = alltData.objects.get(session_id=user_id)

    if res.session_end == 0: #대화 처음 시작
        data = dialogflow(msg_str, user_id)
        txt += str(data['result']['metadata']['intentName'])
        incom = str(data['result']['actionIncomplete'])

        if eq(incom, "True"): #대화 세션 유지, session_end를 1로
            txt += str(data['result']['fulfillment']['speech'])
            alltData(session_id=user_id, session_end=1, jsondata=data).save()
        else : #대화 종료, 필수조건 충족, 사용자에게 결과 전송, session_end를 0으로
            alltData(session_id=user_id, session_end=0, jsondata=data).save()
            txt += incomFalse(user_id)
    else : #이전 대화 유지
        data = dialogflow(msg_str, user_id)
        incom = str(data['result']['actionIncomplete'])

        if eq(incom, "True"): #대화 세션 유지, session_end를 1로
            txt += str(data['result']['fulfillment']['speech'])
            alltData(session_id=user_id, session_end=1, jsondata=data).save()
        else : #대화 종료, 필수조건 충족, 사용자에게 결과 전송, session_end를 0으로
            alltData(session_id=user_id, session_end=0, jsondata=data).save()
            txt += incomFalse(user_id)


    return JsonResponse({
        'message':{'text':"!!!\n\n"+txt+"\n\n!!!"},
        'keyboard':{'type':'text'}
    })

def incomFalse(user_id):
    res = alltData.objects.get(session_id=user_id)

    intent_name = res.jsondata['result']['metadata']['intentName']
    text = ""

    #인텐트별로 처리
    if eq(intent_name, "path-finder"):
        text = "\n길을 찾아드릴게요\n"


    return text


# def incomTure():




	# print(res.session_id)

	#write
	#allData(session_id=session_id, jsondata=jsontmp, dialogflow_action=dialogflow).save()

	#read

	#result = allData.objects.get(pk=11111)
	#print("dialgoflow : " + str(result.dialogflow_action))


	#num = allData.objects.filter(session_id=11111).count()
	#txt += "\n\n\npre -> \n"+pData

	#print(num)
