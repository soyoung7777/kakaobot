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
from chat.models import testData

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
	# message = ((request.body).decode('utf-8'))
	# msg = json.loads(message)
	# user_id = msg['user_key']
    # msg_str = msg['content']


    message = ((request.body).decode('utf-8'))
    msg = json.loads(message)
    user_id = msg['user_key']
    msg_str = msg['content']

    num = testData.objects.filter(session_id=user_id).count()

	# jsontmp = "22222"
	# dialogflow = 2

	# num = testData.objects.filter(session_id=user_id).count()
    txt = ""

    if num == 0: # 처음
        testData(session_id=user_id).save()
    #else:

    res = testData.objects.get(session_id=user_id)[0]

    if res.session_end == 0:
        data = dialgoflow(msg_str, user_id)
        testData(session_id=user_id, session_end=1, msg=msg_str, jsondata=data).save()
        txt += str(data['result']['metadata']['intentName'])
    else :
        txt += "session_end가 1\n"

    return JsonResponse({
        'message':{'text':"!!!\n\n"+txt+"\n\n!!!"},
        'keyboard':{'type':'text'}
    })



	# print(res.session_id)

	#write
	#allData(session_id=session_id, jsondata=jsontmp, dialogflow_action=dialogflow).save()

	#read

	#result = allData.objects.get(pk=11111)
	#print("dialgoflow : " + str(result.dialogflow_action))


	#num = allData.objects.filter(session_id=11111).count()
	#txt += "\n\n\npre -> \n"+pData

	#print(num)
