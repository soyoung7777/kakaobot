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

CLIENT_ACCESS_TOKEN = 'f087d3e9915f48e9935bba49078b7d83'
#CLIENT_ACCESS_TOKEN = '33615c11c39546908fd8ab5b32dfac16'
#CLIENT_ACCESS_TOKEN = '72906773549e43b2b2fe92dcdd24abe7'



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
    # DB.dialogflow_action = 0
    # DB.subway_action=0

    #다른경로
    if DB.diff_path is not 0:
        cur_time = str(time.time())
        if eq(msg_str,"Y") or eq(msg_str,"y") or eq(msg_str,"ㅇ") or eq(msg_str,"응") or eq(msg_str,"어"):
            if cur_time > DB.limit_time:
                text =  "시간이 지났어요!!\n다시 경로를 찾아주세요"
                DB.diff_path = 0
                DB.save()
                return JsonResponse({
                    'message': {'text': text},
                })
            else:
                data = json.loads(json.dumps(ast.literal_eval(str(DB.jsondata))))
                if eq(str(data['result']['metadata']['intentName']),"PathFind"):
                    start = str(data['result']['parameters']['all_from'])
                    end = str(data['result']['parameters']['all_to'])
                    text = pathPrint.get_result(start, end, '', DB.diff_path)

                    if not eq(text[0],"더"):
                        DB.diff_path += 1
                        DB.limit_time = time.time() + 10
                        DB.save()

                    return JsonResponse({
                    'message': {'text': text},
                    })


    #dialog_data = dialogflow(msg_str)
    if eq(msg_str,"초기화"):
        DB.dialogflow_action = 0
        DB.subway_action = 0
        DB.subway_selected = ""
        DB.subway_station_name=""
        DB.dialogflow_action = 0
        DB.bus_action = 0
        DB.bus_arsid = ""
        DB.bus_selected = ""
        DB.bus_station_result = ""
        DB.jsondata = ""
        DB.diff_path = 0
        DB.limit_time = ""
        DB.save()

        return JsonResponse({
            'message': {'text': "💜저는 교통정보를 알려주는 ’내가알려줄지도’ 입니다. 🤖💜\n\n"+
            "제가 할 수 있는 일은\n"+
            "①경로 검색 \n"+
            "②실시간 교통정보 검색  입니다!\n"+
            "‘도움말’을 채팅창에 입력하시면,\n"+
            "저를 사용하는 방법을 알려드립니다! 😆\n"+
            "친구 추가해주셔서 감사합니다.\n"+
            "오늘도 좋은 하루 보내세요 ❤️"}
        })
    # if eq((dialog_data['result']['metadata']['intentName']),"Help"):
    #     print("Intent : Help")
    #     text = str(dialog_data['result']['fulfillment']['messages'][0]['speech'])
    #     return JsonResponse({
    #     'message': {'text': text},
    #     })
    # if eq((dialog_data['result']['metadata']['intentName']),"Default Fallback Intent"):
    #     print("Intent : Default Fallback intent")
    #     text = str(dialog_data['result']['fulfillment']['messages'][0]['speech'])
    #     return JsonResponse({
    #     'message': {'text': text},
    #     })
    if DB.dialogflow_action == 0 :
        dialog_data = dialogflow(msg_str)
        print("============dialog_data==============")
        print(str(dialog_data))
        print("status : " + str(dialog_data['result']['actionIncomplete']))

        if eq((dialog_data['result']['actionIncomplete']),"True") :
            print("True")
            DB.jsondata = dialog_data
            DB.save()
            text = str(dialog_data['result']['fulfillment']['speech'])
            return JsonResponse({
                'message': {'text':text},
            })
        if eq((dialog_data['result']['metadata']['intentName']),"Help"):
            print("Intent : Help")
            text = str(dialog_data['result']['fulfillment']['messages'][0]['speech'])
            return JsonResponse({
            'message': {'text': text},
            })
        if eq((dialog_data['result']['metadata']['intentName']),"Default Fallback Intent"):
            print("Intent : Default Fallback intent")
            text = str(dialog_data['result']['fulfillment']['messages'][0]['speech'])
            return JsonResponse({
            'message': {'text': text},
            })

        DB.jsondata = dialog_data
        DB.save()


    data = json.loads(json.dumps(ast.literal_eval(str(DB.jsondata))))
    print(data)


    if DB.dialogflow_action == 1 :
        print("dialog flow action = 1")
        if eq(data['result']['metadata']['intentName'],"Bus_station"):
            if DB.bus_action == 1 :
                tmp_list = DB.bus_station_result
                tmp_list = tmp_list.replace('[',"")
                tmp_list = tmp_list.replace(']',"")
                tmp_list = tmp_list.replace(' ',"")
                bus_station_result = tmp_list.split(',')
                try:
                    DB.bus_selected = bus_station_result[int(msg_str)-1]
                except ValueError:
                    DB.dialogflow_action = 0
                    DB.bus_action = 0
                    DB.bus_arsid = ""
                    DB.bus_selected = ""
                    DB.bus_station_result = ""
                    DB.jsondata = ""
                    DB.save()
                    return JsonResponse({
                    'message': {'text': "잘못된 입력입니다😂처음부터 다시 시작해주세요!"},
                    })
                except IndexError:
                    DB.dialogflow_action = 0
                    DB.bus_action = 0
                    DB.bus_arsid = ""
                    DB.bus_selected = ""
                    DB.bus_station_result = ""
                    DB.jsondata = ""
                    DB.save()
                    return JsonResponse({
                    'message': {'text': "잘못된 입력입니다😂처음부터 다시 시작해주세요!"},
                    })
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
                try:
                    DB.subway_selected = subway_station_result[int(msg_str)-1]
                except ValueError:
                    DB.dialogflow_action = 0
                    DB.subway_action = 0
                    DB.subway_selected = ""
                    DB.subway_station_name=""
                    DB.jsondata = ""
                    DB.save()
                    return JsonResponse({
                    'message': {'text': "잘못된 입력입니다😂처음부터 다시 시작해주세요!"},
                    })
                except IndexError:
                    DB.dialogflow_action = 0
                    DB.subway_action = 0
                    DB.subway_selected = ""
                    DB.subway_station_name=""
                    DB.jsondata = ""
                    DB.save()
                    return JsonResponse({
                    'message': {'text': "잘못된 입력입니다😂처음부터 다시 시작해주세요!"},
                    })
                print(DB.subway_selected)
                DB.subway_action = 2
                DB.dialogflow_action = 0
                DB.save()
    #if(dialogflow_action == 1)문 종료

    if eq(str(data['result']['metadata']['intentName']),"PathFind"):
        DB.diff_path = 0
        start = str(data['result']['parameters']['all_from'])
        end = str(data['result']['parameters']['all_to'])
        text = start+"에서 "+end+"까지 가는 길 알려드릴게요!\n\n\n"
        text += pathPrint.get_result(start, end, '', DB.diff_path)

        if not eq(text[0],"더"):
            DB.diff_path += 1
            DB.limit_time = time.time() + 10
            DB.save()

        return JsonResponse({
            'message': {'text': text,
                        'message_button': {'label':"자세히 보기",'url':"https://sihyun0107.github.io/kakaobotWeb/Website/index.html"}
                    },
        })


    if eq(str(data['result']['metadata']['intentName']),"PathFind_transportation"):
            start = str(data['result']['parameters']['all_from'])
            end = str(data['result']['parameters']['all_to'])
            tsType = str(data['result']['parameters']['transportation'])
            if eq(tsType,"지하철") or eq(tsType,"버스"):
                text = pathPrint.get_result(start, end, tsType, DB.diff_path)
            elif eq(tsType,"고속버스") or eq(tsType,"시외버스"):
                text = anotherPathPrint.get_result(start, end, tsType)

            if not eq(text[0],"더"):
                DB.diff_path += 1
                DB.limit_time = time.time() + 10
                DB.save()

            return JsonResponse({
                'message': {'text': text},
            })

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
                'message': {'text': text},
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
                'message': {'text': text},
                })

    if eq(str(data['result']['metadata']['intentName']),"Subway_station_and_number"):
        print("Intent : Subway_station_and_number")
        Exist = SubwayInfo.config_exist_subway_station_and_number([data['result']['parameters']['subway_station'],
        data['result']['parameters']['subway_number']])

        if Exist:
            res = SubwayInfo.get_subway_station_and_number_information([data['result']['parameters']['subway_station'],
            data['result']['parameters']['subway_number']])
            return JsonResponse({
            'message': {'text': res},
            })
        else:
            return JsonResponse({
            'message': {'text': "정확한 지하철 역명과 호선을 입력해주세요😂"},
            })

    if eq(str(data['result']['metadata']['intentName']),"Subway_station"):
        print("Intent : Subway_station")
        print("subway action : "+str(DB.subway_action))
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
                'message': {'text': text},
                })

    # if eq(str(data['result']['metadata']['intentName']),"Help"):
    #     print("Intent : Help")
    #     text = str(data['result']['fulfillment']['messages'][0]['speech'])
    #     return JsonResponse({
    #     'message': {'text': text},
    #     })
    # if eq(str(data['result']['metadata']['intentName']),"Default Fallback Intent"):
    #     print("Intent : Default Fallback intent")
    #     text = str(data['result']['fulfillment']['messages'][0]['speech'])
    #     return JsonResponse({
    #     'message': {'text': text},
    #     })
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

    if eq(str(data['result']['metadata']['intentName']),"Help"):
        text = str(data['result']['fulfillmentText'])
        return JsonResponse({
        'message': {'text': text},
        })
    if eq(str(data['result']['metadata']['intentName']),"Default Fallback intent"):
        text = str(data['result']['fulfillment']['messages'][0]['speech'])
        return JsonResponse({
        'message': {'text': text},
        })
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
        #data['result']['parameters']['subway_number']])

        #if Exist:
        subway_number = DB.subway_selected
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


    return JsonResponse({
        'message':{'text':txt},
        'keyboard':{'type':'text'}
    })
