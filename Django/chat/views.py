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
import ast

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
#CLIENT_ACCESS_TOKEN = '33615c11c39546908fd8ab5b32dfac16'
CLIENT_ACCESS_TOKEN = '72906773549e43b2b2fe92dcdd24abe7'



def dialogflow(msg_str):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    dialogflow_request = ai.text_request()

    dialogflow_request.lang = 'ko'
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

    num = allData.objects.filter(session_id=user_id).count()
    print("count : " + str(num))
    print("user_id : " + user_id)

    txt = ""

    if num == 0: # 처음
        allData(session_id=user_id).save()
    #else:

    DB = allData.objects.get(pk=user_id)
    print("DB check : " + str(DB.session_id))
    DB.dialogflow_action = 0
    if DB.dialogflow_action == 0 :
        dialog_data = dialogflow(msg_str)
        print("status : " + str(dialog_data['result']['actionIncomplete']))

        if eq((dialog_data['result']['actionIncomplete']),"True") :
            print("True")
            DB.jsondata = dialog_data
            DB.save()
            text = str(dialog_data['result']['fulfillment']['speech'])
            return JsonResponse({
                'message': {'text': "!!!\n"+text+"\n\n!!!"},
            })

        DB.jsondata = dialog_data
        DB.save()


    data = json.loads(json.dumps(ast.literal_eval(str(DB.jsondata))))
    print(data)
    if DB.dialogflow_action == 1 :
        print("dialogflow action = 1")
        if eq(data['result']['metadata']['intentName'],"Bus_station"):
            if DB.bus_action == 1 :
                tmp_list = DB.bus_station_result
                tmp_list = tmp_list.replace('[',"")
                tmp_list = tmp_list.replace(']',"")
                tmp_list = tmp_list.replace(' ',"")
                bus_station_result = tmp_list.split(',')
                DB.bus_selected = bus_station_result[int(msg_str)-1]
                print(DB.bus_selected)
                DB.bus_action = 2
                DB.dialogflow_action = 0
                DB.save()

        if eq(str(data['result']['metadata']['intentName']),"Bus_station_and_number") :
            if DB.bus_action == 1 :
                tmp_list = DB.bus_station_result
                tmp_list = tmp_list.replace('[',"")
                tmp_list = tmp_list.replace(']',"")
                tmp_list = tmp_list.replace(' ',"")
                bus_station_result = tmp_list.split(',')
                DB.bus_selected = bus_station_result[int(msg_str)-1]
                print(DB.bus_selected)
                DB.bus_action = 2
                DB.dialogflow_action = 0
                DB.save()

        if eq(str(data['result']['metadata']['intentName']),"Subway_station") :
            if DB.subway_action == 1 :
                tmp_list = DB.subway_station_result
                tmp_list = tmp_list.replace('[',"")
                tmp_list = tmp_list.replace(']',"")
                subway_station_result = tmp_list.split(',')
                DB.subway_selected = subway_station_result[int(msg_str)-1]
                print(DB.subway_selected)
                DB.subway_action = 2
                DB.dialogflow_action = 0
                DB.save()

    if eq(str(data['result']['metadata']['intentName']),"Bus_station"):
        if DB.bus_action == 0 :
            print("action 0")
            bus_return = BusInfo.get_bus_station(data)

            if bus_return[0] == 1 :
                DB.bus_selected = str(bus_return[2][0])
                DB.bus_arsid = str(bus_return[3])
                DB.bus_action = 2
                DB.save()

            elif bus_return[0] == 2 :
                print("action1")
                DB.bus_action = 1
                text = bus_return[1]
                DB.bus_arsid = bus_return[3]
                DB.bus_station_result = bus_return[2]
                DB.dialogflow_action = 1
                DB.save()

                return JsonResponse({
                'message': {'text': "!!!\n"+text+"\n\n!!!"},
                })

    if eq(str(data['result']['metadata']['intentName']),"Bus_station_and_number"):
        if DB.bus_action == 0 :
            print("action 0")
            bus_return = BusInfo.get_bus_station(data)

            if bus_return[0] == 1 :
                DB.bus_selected = str(bus_return[2][0])
                DB.bus_arsid = str(bus_return[3])
                DB.bus_action = 2
                DB.save()

            elif bus_return[0] == 2 :
                print("action1")
                DB.bus_action = 1
                text = bus_return[1]
                DB.bus_arsid = bus_return[3]
                DB.bus_station_result = bus_return[2]
                DB.dialogflow_action = 1
                DB.save()

                return JsonResponse({
                'message': {'text': "!!!\n"+text+"\n\n!!!"},
                })
    if eq(str(data['result']['metadata']['intentName']),"Subway_station_and_number"):
        print("Intent : Subway_station_and_number")
        Exist = SubwayInfo.config_exist_subway_station_and_number([data['result']['parameters']['subway_station'],
        data['result']['parameters']['line_number']])

        if Exist:
            res = SubwayInfo.get_subway_station_and_number_information([data['result']['parameters']['subway_station'],
            data['result']['parameters']['line_number']])
            return JsonResponse({
            'message': {'text': res},
            })
        else:
            return JsonResponse({
            'message': {'text': "정확한 지하철 역명과 호선을 입력해주세요"},
            })
    if eq(str(data['result']['metadata']['intentName']),"Subway_station"):
        print("Intent : Subway_station")
        DB.subway_action=0
        if DB.subway_action == 0 :
            print("action 0")
            subway_return = SubwayInfo.get_subway_station(data)

            if subway_return[0] == 1 :#해당 역에 호선이 1개만 있는 경우
                print("subway action2")
                DB.subway_selected = str(subway_return[2][0])
                DB.subway_action = 2
                DB.subway_station_name = data['result']['parameters']['subway_station']
                DB.save()

            elif subway_return[0] == 2 :#해당 역에 호선이 여러개 있는 경우
                print("subway action1")
                DB.subway_action = 1
                DB.subway_station_name = data['result']['parameters']['subway_station']
                DB.subway_station_result =subway_return[2]
                text = subway_return[1]
                # DB.bus_station_result = bus_return[2]
                DB.dialogflow_action = 1
                DB.save()

                return JsonResponse({
                'message': {'text': "!!!\n"+text+"\n\n!!!"},
                })
        #print("subway action : "+str(DB.subway_action))
        #DB.subway_action = 0
        #if DB.subway_action == 0 :
            #print("subway action 0")
        #subway_return = SubwayInfo.get_subway_station(data)

            # if subway_return[0] == 1 :
            #     print("subway action 2")
            #     DB.subway_selected = str(subway_return[2][0])
            #     DB.subway_stationid = str(subway_return[3])
            #     DB.subway_action = 2
            #     DB.save()

            # if subway_return[0] == 2 :
            #     print("subway action 1")
            #     DB.subway_action = 1
            #     text = subway_return[1]
            #     DB.subway_stationid = subway_return[3]
            #     DB.subway_station_result = subway_return[2]
            #     DB.dialogflow_action = 1
            #     DB.save()
            #
            #     return JsonResponse({
            #     'message': {'text': "!!!\n"+text+"\n\n!!!"},
            #     })

    if DB.bus_action == 2 :
        print("action2")
        if eq(str(data['result']['metadata']['intentName']),"Bus_station") :
            res = BusInfo.get_bus_station_information([DB.bus_selected,DB.bus_arsid])
        elif eq(str(data['result']['metadata']['intentName']),"Bus_station_and_number") :
            res = BusInfo.get_bus_station_and_number_information([DB.bus_selected,DB.bus_arsid,data['result']['parameters']['bus_number']])

        DB.dialogflow_action = 0
        DB.bus_action = 0
        DB.bus_arsid = ""
        DB.bus_selected = ""
        DB.bus_station_result = ""
        DB.jsondata = ""
        DB.save()

        return JsonResponse({
        'message': {'text': res},
        })

    if DB.subway_action == 2 :
        print("subway action 2")
        #Exist = SubwayInfo.config_exist_subway_station_and_number([data['result']['parameters']['subway_station'],
        #data['result']['parameters']['line_number']])

        #if Exist:
        line_number = DB.subway_selected
        line_number = line_number.replace('수도권',"")
        res = SubwayInfo.get_subway_station_and_number_information([DB.subway_station_name,
        DB.subway_selected])

        DB.dialogflow_action = 0
        DB.subway_action = 0
        DB.subway_selected = ""
        DB.subway_station_name=""
        DB.save()

        return JsonResponse({
        'message': {'text': res},
        })

    # return JsonResponse({
    #     'message':{'text':"!!!\n\n"+txt+"\n\n!!!"},
    #     'keyboard':{'type':'text'}
    # })

    # if DB.subway_action == 2 :
    #     print("action2")
    #     # if eq(str(data['result']['metadata']['intentName']),"Bus_station") :
    #     #     res = BusInfo.get_bus_station_information([DB.bus_selected,DB.bus_arsid])
    #     if eq(str(data['result']['metadata']['intentName']),"Subway_station_and_number") :
    #         res = SubwayInfo.get_subway_station_and_number_information([DB.subway_selected,DB.subway_stationid,data['result']['parameters']['line_number']])
    #     print(res)
    #     DB.dialogflow_action = 0
    #     DB.subway_action = 0
    #     DB.subway_stationid = ""
    #     DB.subway_selected = ""
    #     DB.subway_station_result = ""
    #     DB.jsondata = ""
    #     DB.save()
    #
    #     return JsonResponse({
    #     'message': {'text': res},
    #     })


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
