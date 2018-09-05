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

def dialogflow(msg_str):
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

init = True

@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))

	if init :
		session_id = randrange(9999,100000)
		init = False

	msg = json.loads(message)
	jsontmp = "22222"
	dialogflow = 2

	#write
	allData(session_id=session_id, jsondata=jsontmp, dialogflow_action=dialogflow).save()

	#read

	result = allData.objects.get(pk=11111)
	print("dialgoflow : " + str(result.dialogflow_action))

	
	num = allData.objects.filter(session_id=11111).count()
	#txt += "\n\n\npre -> \n"+pData

	print(num)

	return JsonResponse({
		'message':{'text':"!!!\n\n"+str(session_id)+"\n\n!!!"},
		'keyboard':{'type':'text'}
		})
