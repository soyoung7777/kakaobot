#subway_return = SubwayInfo.get_subway_station(data)
import json
import urllib.request
import urllib.parse
import ast
import re
import time
from operator import eq
from datetime import datetime
subwayID = [[1001, "수도권 1호선"],[1002, "수도권 2호선"],[1003, "수도권 3호선"],[1004, "수도권 4호선"],[1005, "수도권 5호선"]
,[1006, "수도권 6호선"],[1007, "수도권 7호선"],[1008, "수도권 8호선"],[1009, "수도권 9호선"],[1065,"수도권 공항철도"]
,[1071,"수도권 수인선"],[1075,"수도권 분당선"],[1063,"수도권 경의중앙선"],[1067,"수도권 경춘선"],[1077,"수도권 신분당선"]]

def get_subway_station(json_Data):
    searchST = str(json_Data['result']['parameters']['subway_station'])

    if eq(searchST, "총신대입구(이수)"):
        subway_station_list = ["수도권 4호선", "수도권 7호선"]
        res = "🤔 호선을 선택해 주세요. 🤗" + "\n"+"(올바른 숫자를 입력하는 센스!)\n\n"
        for idx, line_number in enumerate(subway_station_list):
            res += str(idx+1) +". " + line_number + "\n"
        return [2,res,subway_station_list]

    searchST = re.sub('\((.*?)\)','',searchST)
    # searchST2 = re.search('\((.*?)\)',searchST).group()
    # searchST2 = re.sub("^\(","",searchST2)
    # searchST2 = re.sub("\)","",searchST2)

    print("searchST " + searchST)
    # print("searchST1 " + searchST1)
    # print("searchST2 " + searchST2)

    # searchStation = []
    # searchStation.append(searchST1)
    # searchStation.append(searchST2)

    # print("searchStation : "+str(searchStation))
    res = ""
    ACCESS = "rxJqZMHh6oQDUSfc7Kh42uCXZuHEhmj7dY7VWber2ryr9L5t2CFRy3z834JMR7RygMzaVby7ZQ3sW%2ByCZZn0Ig%3D%3D"
    my = "n+1iCTjka3qgrhco9Xl3e05Depf0hpct6SJUYUEH38E"
    encMy = urllib.parse.quote_plus(my)

    #for s in searchStation:
    encST = urllib.parse.quote_plus(searchST)

    odUrl = "https://api.odsay.com/v1/api/searchStation?lang=0&stationName="+encST+"&CID=1000&stationClass=2&apiKey="+encMy

    request = urllib.request.Request(odUrl)
    response = urllib.request.urlopen(request)

    json_rt = response.read().decode('utf-8')
    st = json.loads(json_rt)

    subway_station_list = []
    for i in range(0,len(st['result']['station'])):
        if st['result']['station'][i]['stationName'] == searchST:
            subway_station_list.append(st['result']['station'][i]['laneName'])

    #subway_station_list = list(set(subway_station_list))

    print(str(subway_station_list))
    print(str(len(subway_station_list)))
    if len(subway_station_list) == 1 :
        return [1,res,subway_station_list]

    else :
        res += "🤔 호선을 선택해 주세요. 🤗" + "\n"+"(올바른 숫자를 입력하는 센스!)\n\n"
        for idx, line_number in enumerate(subway_station_list):
            res += str(idx+1) +". " + line_number + "\n"
        return [2,res,subway_station_list]
#
#     res = ""
#     duplicate = False
#     stationName = str(json_Data['result']['parameters']['subway_station'])
#     # line_number = str(json_Data['result']['parameters']['line_number'])
#     SNList = [["반포역", "신반포역", "구반포역"], ["논현역", "신논현역"], ["뚝섬역", "뚝섬유원지역"]]
#
#     subway_station_dic = {}
#     print("입력한 역이름 :"+stationName)
#     for e in SNList:
#         if stationName in e:
#             duplicate = True#선택사항 존재
#             for s in e:
#                 data = getStationInfo(s)
#                 subway_station_dic[s].append(int(data['result']['station'][0]['stationID']))
#
#     if duplicate == False:
#         data = getStationInfo(stationName)
#         print(data)
#         subway_station_dic[stationName] = int(data['result']['station'][0]['stationID'])
#
#     if len(subway_station_dic.keys()) == 1:
#         return[1,res,list(subway_station_dic.keys()), subway_station_dic]
#     else:
#         res += "🤔 지하철 역을 선택해 주세요. 🤗" + "\n"
#         for i in range(0, len(subway_station_dic.keys())):
#             res += str(i+1)+". "+list(subway_station_dic.keys())[i]+"\n"
#         return [2,res,list(subway_station_dic.keys()),subway_station_dic]

# def get_result(stationName, line_number):
def config_exist_subway_station_and_number(subwayData):
    stationName = subwayData[0]
    #data = getStationInfo(stationName)
    #station_info = data['result']['station']
    with open('/home/ubuntu/Django/chat/SubwayLineMap.json', encoding='utf-8') as f:
        subwaylinemap = json.load(f)
    laneID = getLaneID(subwayData[1])
    subwaylinemap = subwaylinemap[str(laneID)]
    #print(str(subwaylinemap))
    Exist = False
    for item in subwaylinemap:
        #print(str(item))
        #for key, value in item.items():
        if eq(stationName,item):
            Exist = True
            break
    #for idx, info in enumerate(station_info):
        #if subwayData[1] in info['laneName'] and stationName in info['stationName']:
            #Exist = True
    return Exist

def simple_get_subway_station_and_number_information(subwayData):
    print("=========get simple============")
    day = getDayType()
    stationName = subwayData[0]
    subwayData[1] = re.sub('\'',"",subwayData[1])
    subwayData[1] = re.sub('수도권 ',"",subwayData[1])
    subwayData[1] = subwayData[1].strip()
    print("stationName : "+subwayData[0])
    print("lineNumber : "+subwayData[1])
    #print("lineNumber type : "+str(type(subwayData[1])))

    if eq(subwayData[0], "총신대입구(이수)") and eq(subwayData[1],"7호선"):
        current_laneID = 1007
        current_laneName = "수도권 7호선"
        stationName = "총신대입구(이수)"

    else:
        data = getStationInfo(stationName)

        station_info = data['result']['station']
        #current_stationID = 0

        #print(json.loads(json.dumps(data)))
        # print("station Dictionary : "+str(subwayData[1]))
        # print("station Dictionary type: "+str(type(subwayData[1])))
        # print("station ID : "+str(subwayData[1][subwayData[0]]))

        #print("laneName(subwayData[1]) : "+subwayData[1])

        if not eq(subwayData[1],"경의중앙선") and "수도권" not in subwayData[1]:
            subwayData[1] = "수도권 "+subwayData[1]

        #print("laneName(subwayData[1]) : "+subwayData[1])
        #print(str(station_info))
        for idx, info in enumerate(station_info):
            #print(str(info))
            if subwayData[1] in info['laneName'] or subwayData[1] in str(info['laneName']):
                #current_stationID = int(data['result']['station'][idx]['stationID'])
                current_laneName = data['result']['station'][idx]['laneName'] #예:수도권 1호선
                break


        current_laneID = getLaneID(current_laneName)
    #print("current_laneName : "+current_laneName)
    #print("current_laneID : "+str(current_laneID))
    #line_number = subwayData[1]
    #if eq(direction,"상행") or eq(direction,"내선"):
    # with open('/home/ubuntu/Django/chat/SubwayStationID.json', encoding='utf-8') as f:
    #     subwaystationid = json.load(f)
    # subwaystationid = subwaystationid[str(current_laneID)]
    with open('/home/ubuntu/Django/chat/SubwayLineMap.json', encoding='utf-8') as f:
        subwaylinemap = json.load(f)

    subwaylinemap = subwaylinemap[str(current_laneID)]
    #print("subwaylinemap : "+str(subwaylinemap))
    #current_subwaylinemap = getLineMap(stationName,subwaylinemap)
    current_subwaylinemap = subwaylinemap[stationName]
    #print("current_subwaylinemap : "+str(current_subwaylinemap))

    text=""
    direction = []
    direction_stationlist = []
    StationExistNameList = []

    for item in current_subwaylinemap:
        for key, value in item.items():
            direction.append(key)
            direction_stationlist.append(value)
    direction = list(set(direction))
    print("direction : "+str(direction))
    for d in direction:
        #print("방향 : "+d)
        #print("괄호안 : "+re.search('\((.*?)\)',d).group())
        if eq("(상행)",re.search('\((.*?)\)',d).group()) or eq("(외선)",re.search('\((.*?)\)',d).group()):
            print("상행이나 외선")
            try:
                StationExistName,TrainDirection = getStationExistSimple(stationName, current_laneID, 1)
                if eq(StationExistName, "error"):
                    print("error")
                    #text+="공공데이터에 문제가 생겼어요😂😂\n\n[시간표 정보로 안내합니다]\n\n"
                    text +="💌["+d+"]💌\n"
                    text +=simple_get_schedule(stationName, day, 1,current_laneName)+"\n\n"
                    #text +="공공데이터에 문제가 생겼어요😂😂\n10초 뒤에 다시 이용해주시겠어요?\n꼭 다시 오셔야해요❤"

                elif eq(StationExistName, "none"):
                    print("none")
                    text +="💌["+d+"]💌\n"
                    text +=simple_get_schedule(stationName, day, 1,current_laneName)+"\n\n"
                    #text +="해당 정보는 공공데이터에서 알려주지 않고 있어요😂😂\n다른 정보를 검색해보세요❤"
                else:
                    #text +=simple_get_schedule(stationName, day, 1,current_laneName)
                    text +="💌["+d+"]💌\n"
                    text +=TrainDirection+"\n"
                    text +=StationExistName+"\n\n"
            except:
                print("except")
                text+="공공데이터에 문제가 생겼어요😂😂\n\n[시간표 정보로 안내합니다]\n"
                text +="💌["+d+"]💌\n\n"
                text +=simple_get_schedule(stationName, day, 1,current_laneName)
                #text +="공공데이터에 문제가 생겼어요😂😂\n10초 뒤에 다시 이용해주시겠어요?\n꼭 다시 오셔야해요❤"
                return text

        else:
            print("하행이나 내선")
        #text +="💌["+stationName+" "+current_laneName+" "+direction[-1]+"]💌\n"
            try:
                StationExistName,TrainDirection = getStationExistSimple(stationName, current_laneID, 2)
                if eq(StationExistName, "error"):
                    print("error")
                    #text+="공공데이터에 문제가 생겼어요😂😂\n\n[시간표 정보로 안내합니다]\n"
                    text +="💌["+d+"]💌\n"
                    #text +="공공데이터에 문제가 생겼어요😂😂\n10초 뒤에 다시 이용해주시겠어요?\n꼭 다시 오셔야해요❤"
                    text +=simple_get_schedule(stationName, day, 2,current_laneName)+"\n\n"
                elif eq(StationExistName, "none"):
                    print("none")
                    text +="💌["+d+"]💌\n"
                    text +=simple_get_schedule(stationName, day, 2,current_laneName)+"\n\n"
                    #text +="해당 정보는 공공데이터에서 알려주지 않고 있어요😂😂\n다른 정보를 검색해보세요❤"
                else:
                    #text +=simple_get_schedule(stationName, day, 2,current_laneName)

                    text +="💌["+d+"]💌\n"
                    text +=TrainDirection+"\n"
                    text +=StationExistName+"\n\n"
            except:
                print("except")
                #text +="공공데이터에 문제가 생겼어요😂😂\n10초 뒤에 다시 이용해주시겠어요?\n꼭 다시 오셔야해요❤"
                text +="💌["+d+"]💌\n\n"
                text +=simple_get_schedule(stationName, day, 2,current_laneName)
                return text



    print("======simple========\n"+text)
    return text

def detail_get_subway_station_and_number_information(subwayData):
    print("===========get detail========")
    day = getDayType()
    stationName = subwayData[0]
    subwayData[1] = re.sub('\'',"",subwayData[1])
    subwayData[1] = re.sub('수도권 ',"",subwayData[1])
    subwayData[1] = subwayData[1].strip()
    print("stationName : "+subwayData[0])
    print("lineNumber : "+subwayData[1])
    #print("lineNumber type : "+str(type(subwayData[1])))

    if eq(subwayData[0], "총신대입구(이수)") and eq(subwayData[1],"7호선"):
        current_laneID = 1007
        current_laneName = "수도권 7호선"
        stationName = "총신대입구(이수)"

    else:
        data = getStationInfo(stationName)

        station_info = data['result']['station']
        #current_stationID = 0

        #print(json.loads(json.dumps(data)))
        # print("station Dictionary : "+str(subwayData[1]))
        # print("station Dictionary type: "+str(type(subwayData[1])))
        # print("station ID : "+str(subwayData[1][subwayData[0]]))

        #print("laneName(subwayData[1]) : "+subwayData[1])

        if not eq(subwayData[1],"경의중앙선") and "수도권" not in subwayData[1]:
            subwayData[1] = "수도권 "+subwayData[1]

        #print("laneName(subwayData[1]) : "+subwayData[1])
        #print(str(station_info))
        for idx, info in enumerate(station_info):
            #print(str(info))
            if subwayData[1] in info['laneName'] or subwayData[1] in str(info['laneName']):
                #current_stationID = int(data['result']['station'][idx]['stationID'])
                current_laneName = data['result']['station'][idx]['laneName'] #예:수도권 1호선
                break


        current_laneID = getLaneID(current_laneName)
    #print("current_laneName : "+current_laneName)
    #print("current_laneID : "+str(current_laneID))
    #line_number = subwayData[1]
    #if eq(direction,"상행") or eq(direction,"내선"):
    # with open('/home/ubuntu/Django/chat/SubwayStationID.json', encoding='utf-8') as f:
    #     subwaystationid = json.load(f)
    # subwaystationid = subwaystationid[str(current_laneID)]
    with open('/home/ubuntu/Django/chat/SubwayLineMap.json', encoding='utf-8') as f:
        subwaylinemap = json.load(f)
    subwaylinemap = subwaylinemap[str(current_laneID)]
    #print("subwaylinemap : "+str(subwaylinemap))
    #current_subwaylinemap = getLineMap(stationName,subwaylinemap)
    current_subwaylinemap = subwaylinemap[stationName]
    #print("current_subwaylinemap : "+str(current_subwaylinemap))

    text=""
    direction = []
    direction_stationlist = []
    StationExistNameList = []
    sName = re.sub('\((.*?)\)','',stationName)

    if eq(sName,"서울역"):
        title=sName+" "+current_laneName+" 실시간 도착정보"
    else:
        title=sName+"역 "+current_laneName+" 실시간 도착정보"
    for item in current_subwaylinemap:
        for key, value in item.items():
            direction.append(key)
            direction_stationlist.append(value)
    #direction = list(set(direction))
    print("direction : "+str(direction))
    # for d in direction:
    #     if "상행" in d:
    #         StationExistName = getStationExistSimple(stationName, current_laneID, 1)
    #         if eq(StationExistName, "error"):
    #             text +="공공데이터에 문제가 생겼어요😂😂\n10초 뒤에 다시 이용해주시겠어요?\n꼭 다시 오셔야해요❤"
    #             return text
    #         if not eq(StationExistName,"none"):
    #             text +="💌["+d+"]💌\n"
    #             text +=StationExistName+"\n\n"
    #     else:
    #     #text +="💌["+stationName+" "+current_laneName+" "+direction[-1]+"]💌\n"
    #         StationExistName = getStationExistSimple(stationName, current_laneID, 2)
    #         if eq(StationExistName, "error"):
    #             text +="공공데이터에 문제가 녀\n10초 뒤에 다시 이용해주시겠어요?\n꼭 다시 오셔야해요❤"
    #             return text
    #         if not eq(StationExistName,"none"):
    #             text +="💌["+d+"]💌\n"
    #             text +=StationExistName+"\n\n"
    isSchedule = False
    for idx, full_list in enumerate(direction_stationlist):
        text +="<font color='#FF4D45'>"+"💌["+direction[idx]+"]💌"+"</font><br/><br/><br/>"
        for s in full_list:
            #print("====>"+s+"역의 지하철 실시간 도착정보를 알아보자")
            if "상행" in direction[idx]:
                #start_time = time.time()
                StationExistName = getStationExist(s, current_laneID, 1)
                #print("--- %s seconds ---" %(time.time() - start_time))
                #print("StationExistName : "+StationExistName)
                if eq(StationExistName,"error" or "none"):#시간표정보
                    print(stationName+" 상행")
                    text +=detail_get_schedule(stationName, day, 1,current_laneName)
                    text = "<font color='#FF4D45'style='font-weight: bold;line-height:1.5em;'>"+tet+"</font>"
                    isSchedule = True
                    if eq(sName,"서울역"):
                        title=stationName+" "+current_laneName+"시간표 정보"
                    else:
                        title=stationName+"역 "+current_laneName+"시간표 정보"
                    #return title,text
                else:
                    StationExistNameList.append(StationExistName)
                    #print("station Exist Name List : "+str(StationExistNameList))

            else:
                #start_time = time.time()
                StationExistName = getStationExist(s, current_laneID, 2)
                #print("--- %s seconds ---" %(time.time() - start_time))
                #print("StationExistName : "+StationExistName)
                if eq(StationExistName,"error" or "none"):#시간표정보
                    print(stationName+" 하행")
                    text +=detail_get_schedule(stationName, day, 2,current_laneName)
                    text = "<font color='#FF4D45'style='font-weight: bold;line-height:1.5em;'>"+tet+"</font>"
                    isSchedule = True
                    if eq(sName,"서울역"):
                        title=stationName+" "+current_laneName+"시간표 정보"
                    else:
                        title=stationName+"역 "+current_laneName+"시간표 정보"
                else:
                    StationExistNameList.append(StationExistName)
        #print("station Exist Name List : "+str(StationExistNameList))

        StationExistNameList = list(set(StationExistNameList))
        #print("station Exist Name List(no duplicate) : "+str(StationExistNameList))
        if not isSchedule:
            for total in full_list:
                exist = False
                for element in StationExistNameList:
                    if eq(element,total):
                        if eq(total,full_list[-1]):
                            text+="<font color='#FF4D45'style='font-weight: bold;line-height:1.5em;'>"+total+"</font>🚋        "
                        else:
                            text+="<font color='#FF4D45'style='font-weight: bold;line-height:1.5em;'>"+total+"</font>🚋   〰   "
                        exist = True
                if exist==False:
                    # if eq(total,"none"):
                    #     count_end = count_end+1
                    #     continue
                    if eq(total,full_list[-1]):
                        text +="<font style='line-height:1.5em;'>"+total+"</font>"+"        "
                    else:
                        text+="<font style='line-height:1.5em;'>"+total+"</font>"+"   〰   "
            text+="<br/><br/><br/><br/>"
        #text = text.replace("\r\n","<br/>")
        StationExistNameList.clear()
    #print(text)
    return title,text

def getDayType():
    now = time.localtime()
    if 0<=now.tm_wday<=4:#월,화,수,목,금
        return 1
    elif now.tm_wday == 5:#토
        return 2
    elif now.tm_wday == 6:#일
        return 3

def simple_get_schedule(stationName, day, direction, laneName):

    text = ""

    print("stationName : "+stationName)
    #print("day : "+str(day))
    #print("direction : "+str(direction))
    #print("laneName : "+laneName)
    laneName = re.sub("수도권 ","", laneName)
    #print("laneName : "+laneName)
    file_name = ""
    if day == 1:
        file_name+="ord_lane_"+laneName+".json"
    elif day == 2:
        file_name+="sat_lane_"+laneName+".json"
    elif day == 3:
        file_name+="sun_lane_"+laneName+".json"

    print("file name : "+file_name)

    with open('/home/ubuntu/Django/chat/subway_schedule/'+file_name, encoding='utf-8') as f:
        schedule = json.load(f)

    now = datetime.now()
    #hour = now.hour
    print("hour : "+ str(now.hour))
    #print("hour type: "+ str(type(now.hour)))

    if direction ==1:
        time_schedule = schedule[stationName]["up"]
    else:
        time_schedule = schedule[stationName]["down"]

    time_list = ""
    time_exp_list = ""
    for item in time_schedule:
        #print("idx in item : "+str(item["Idx"]))
        if item["Idx"] == now.hour:
            print("item in time schedule : "+str(item))
            print("===schedule===")
            print(str(item["list"]))
            time_list = item["list"]
            if 'expList' in item:
                time_exp_list = item["expList"]

    isExp = False
    print("time_list : "+str(time_list))
    for t in time_list.split(" "):
        tm = re.sub('\((.*?)\)',"",t)
        print("t : "+tm)
        if not eq(tm, "00"):
            tm = tm.lstrip("0")
        print("시간표 시간 : "+tm)
        print("현재 시간 : "+str(now.minute))
        if now.minute <= int(tm):
            Tschedule = t
            if time_exp_list is not "":
                for et in time_exp_list.split(" "):
                    if now.minute < int(re.sub('\((.*?)\)',"",et)) and int(tm) < int(re.sub('\((.*?)\)',"",et)):
                        Tschedule = et
                        isExp = True
            subway_direction =re.search('\((.*?)\)',Tschedule).group()
            subway_direction = re.sub("^\(","",subway_direction)
            subway_direction = re.sub("\)","",subway_direction)

            if isExp:
                text += subway_direction+"행(급행) "+str(now.hour)+"시 "+re.sub('\((.*?)\)',"",Tschedule)+"분 도착 예정"
            else:
                text += subway_direction+"행 "+str(now.hour)+"시 "+re.sub('\((.*?)\)',"",Tschedule)+"분 도착 예정"
            print("==========return text=========")
            return text


    isExp = False
    time_list = ""
    time_exp_list = ""

    for item in time_schedule:
        #print("idx in item : "+str(item["Idx"]))
        if item["Idx"] == now.hour+1:
            print("item in time schedule : "+str(item))
            print("===schedule===")
            print(str(item["list"]))
            time_list = item["list"]
            if 'expList' in item:
                time_exp_list = item["expList"]

    for t in time_list.split(" "):
        tm = re.sub('\((.*?)\)',"",t)
        print("tm : "+tm)
        if not eq(tm, "00"):
            tm = tm.lstrip("0")
        print("시간표 시간 : "+tm)
        print("현재 시간 : "+str(now.minute))
        if now.minute <= int(tm):
            Tschedule = t
            if time_exp_list is not "":
                for et in time_exp_list.split(" "):
                    if now.minute < int(re.sub('\((.*?)\)',"",et)) and int(tm) < int(re.sub('\((.*?)\)',"",et)):
                        Tschedule = et
                        isExp = True
            subway_direction =re.search('\((.*?)\)',Tschedule).group()
            subway_direction = re.sub("^\(","",subway_direction)
            subway_direction = re.sub("\)","",subway_direction)

            if isExp:
                text += subway_direction+"행(급행) "+str(now.hour)+"시 "+re.sub('\((.*?)\)',"",Tschedule)+"분 도착 예정"
            else:
                text += subway_direction+"행 "+str(now.hour)+"시 "+re.sub('\((.*?)\)',"",Tschedule)+"분 도착 예정"
            return text
def detail_get_schedule(stationName, day, direction, laneName):
    #print("stationName : "+stationName)
    #print("day : "+str(day))
    print("direction : "+str(direction))
    #print("laneName : "+laneName)
    laneName = re.sub("수도권 ","", laneName)
    #print("laneName : "+laneName)
    file_name = ""
    if day == 1:
        file_name+="ord_lane_"+laneName+".json"
    elif day == 2:
        file_name+="sat_lane_"+laneName+".json"
    elif day == 3:
        file_name+="sun_lane_"+laneName+".json"

    print("file name : "+file_name)

    with open('/home/ubuntu/Django/chat/subway_schedule/'+file_name, encoding='utf-8') as f:
        schedule = json.load(f)

    now = datetime.now()
    #hour = now.hour
    print("hour : "+ str(now.hour))
    #print("hour type: "+ str(type(now.hour)))

    if direction ==1:
        time_schedule = schedule[stationName]["up"]
    else:
        time_schedule = schedule[stationName]["down"]

    for item in time_schedule:
        print("idx in item : "+str(item["Idx"]))
        if item["Idx"] == now.hour:
            print("item in time schedule : "+str(item))
            print("===schedule===")
            print(str(item["list"]))
            return item["list"]

def getLaneID(laneName):
    print("===get Lane ID function===")
    if "수도권" not in laneName:
        laneName = "수도권 "+laneName
    print("lane Name : "+laneName)

    for (first, last) in subwayID:
        if eq(laneName,last):
            open_data_subwayID = first #예:수도권 4호선인 경우 open_data_subwayID = 1004
    return open_data_subwayID

def getStationInfo(myStationName):
    #print(str(type(myStationName)))
    myStationName = re.sub('\((.*?)\)','',myStationName)
    #print("myStationName : "+myStationName)
    myKey = "n+1iCTjka3qgrhco9Xl3e05Depf0hpct6SJUYUEH38E"
    encKey = urllib.parse.quote_plus(myKey)
    encStationname = urllib.parse.quote_plus(myStationName)
    odUrl = "https://api.odsay.com/v1/api/searchStation?lang=0&stationName="+encStationname+"&stationClass=2&apiKey="+encKey
    request = urllib.request.Request(odUrl)
    response = urllib.request.urlopen(request)

    json_rt = response.read().decode('utf-8')
    data = json.loads(json_rt)
    return data

# def getStationName(stationID):
#     myKey = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
#     encKey = urllib.parse.quote_plus(myKey)
#     encStationID = urllib.parse.quote_plus(str(stationID))
#     odUrl = "https://api.odsay.com/v1/api/subwayStationInfo?lang=0&stationID="+encStationID+"&apiKey="+encKey
#     request = urllib.request.Request(odUrl)
#     response = urllib.request.urlopen(request)
#
#     od_json = response.read().decode('utf-8')
#     od_data = json.loads(od_json)
#     try:
#         stationName = od_data['result']['stationName']
#     except KeyError:
#         return "error"
#     return stationName

def getStationName(stationID, subwaylinemap):
    for key, value in subwaylinemap.items():
        if eq(str(stationID), key):
            return value


# def getStationResult(cID, stationID, stationName, idx, current_laneName,direction,line_number): #예:서울역 수도권 4호선 426
#     for (first, last) in subwayID:
#         if current_laneName == last:
#             open_data_subwayID = first #예:수도권 4호선인 경우 open_data_subwayID = 1004
#
#     open_data_key = "714d78526b7369683130356e4d455357"
#     enckey = urllib.parse.quote_plus(open_data_key)
#
#     stationName = re.sub("[역]$","", stationName)
#
#     encStationname = urllib.parse.quote_plus(stationName)
#     open_data_url = "http://swopenapi.seoul.go.kr/api/subway/"+enckey+"/json/realtimeStationArrival/0/5/"+encStationname
#
#     try:
#         request = urllib.request.Request(open_data_url)
#         response = urllib.request.urlopen(request)
#
#         real_json = response.read().decode('utf-8')
#         real_data = json.loads(real_json)
#         realtimeList = real_data['realtimeArrivalList']
#
#         for list in realtimeList:
#             if list['subwayId'] == str(open_data_subwayID) and list['updnLine']==direction:
#                 if list['arvlMsg2'] == "전역 도착" or list['arvlMsg2'] == "전역 출발":
#                     return idx+1
#                 elif "[" in list['arvlMsg2']:#[5]번째 전역 (화전)
#                     info_str = list['arvlMsg2'].split()
#                     info_str2 = info_str[2]
#                     info_str2 = info_str2[1:len(info_str2)-1]
#
#                     new_data = getStationInfo(info_str2)
#                     new_station_info = new_data['result']['station']
#                     new_stationID = 0
#
#                     for idx, info in enumerate(new_station_info):
#                         if line_number in info['laneName']:
#                             new_stationID = int(new_data['result']['station'][idx]['stationID'])
#
#                     if eq(direction,"상행") or eq(direction,"외선"):
#                         return 6-(new_stationID-cID)
#                     elif eq(direction,"하행") or eq(direction,"내선"):
#                         return cID-new_stationID
#                 elif "(" in list['arvlMsg2']:#3분 58초 후 (삼각지)
#                     my_str = list['arvlMsg2'].split()
#                     for idx,i in enumerate(my_str):
#                         if "(" in i:
#                             my_str2 = my_str[idx]
#
#                     my_str2 = my_str2[1:len(my_str2)-1]
#                     new_data = getStationInfo(my_str2)
#                     new_station_info = new_data['result']['station']
#                     new_stationID = 0
#
#                     for idx, info in enumerate(new_station_info):
#                         if line_number in info['laneName']:
#                             new_stationID = int(new_data['result']['station'][idx]['stationID'])
#
#                     if eq(direction,"상행") or eq(direction,"외선"):
#                         return 6-(new_stationID-cID)
#                     elif eq(direction,"하행") or eq(direction,"내선"):
#                         return cID-new_stationID
#                 else:
#                     return idx
#         return "none"
#     except urllib.error.HTTPError:
#         return "error"
#     except KeyError:
#         return "error"
def getStationExist(stationName, laneID, direction):
    open_data_key = "714d78526b7369683130356e4d455357"
    enckey = urllib.parse.quote_plus(open_data_key)

    #stationName = re.sub('\((.*?)\)','',stationName)
    stationName = re.sub("[역]$","", stationName)
    print("stationName : "+stationName)
    encStationname = urllib.parse.quote_plus(stationName)
    open_data_url = "http://swopenapi.seoul.go.kr/api/subway/"+enckey+"/json/realtimeStationArrival/0/5/"+encStationname
    #print("laneID : "+str(laneID))
    #print("direction : "+str(direction))
    arrivalData={}
    try:
        request = urllib.request.Request(open_data_url)
        response = urllib.request.urlopen(request)

        real_json = response.read().decode('utf-8')
        real_data = json.loads(real_json)
        #print(str(real_data))
        realtimeList = real_data['realtimeArrivalList']
        #print("======realtimeList======")
        #print(str(realtimeList))
        for list in realtimeList:
            #print("========list========\n"+str(list))
            if eq(list['subwayId'],str(laneID)):
                #print("subwayID 일치")
                if direction == 1:#상행 or 외선인 경우
                    #print("상행")
                    if eq(list['updnLine'],'상행') or eq(list['updnLine'],'외선'):
                        arrivalData = list
                        break
                else:
                    #print("하행")
                    if eq(list['updnLine'],'하행') or eq(list['updnLine'],'내선'):
                        arrivalData = list
                        break
        #print("arrival Data : "+str(arrivalData))
        #print("arrival Data type : "+str(type(arrivalData)))

        if not arrivalData:
            print("none!!")
            return "none"
        print("지하철이 어디에 있을까???"+arrivalData['arvlMsg3'])
        return arrivalData['arvlMsg3']
    except urllib.error.HTTPError:
        print("error!!")
        return "error"

def getStationExistSimple(stationName, laneID, direction):
    open_data_key = "714d78526b7369683130356e4d455357"
    enckey = urllib.parse.quote_plus(open_data_key)

    stationName = re.sub("[역]$","", stationName)

    encStationname = urllib.parse.quote_plus(stationName)
    open_data_url = "http://swopenapi.seoul.go.kr/api/subway/"+enckey+"/json/realtimeStationArrival/0/5/"+encStationname
    #print("laneID : "+str(laneID))
    #print("direction : "+str(direction))
    arrivalData={}
    try:
        request = urllib.request.Request(open_data_url)
        response = urllib.request.urlopen(request)

        real_json = response.read().decode('utf-8')
        real_data = json.loads(real_json)
        realtimeList = real_data['realtimeArrivalList']
        #print("======realtimeList======")
        #print(str(realtimeList))
        for rlist in realtimeList:
            #print("========list========\n"+str(rlist))
            if eq(rlist['subwayId'],str(laneID)):
                #print("subwayID 일치")
                if direction == 1:#상행 or 외선인 경우
                    # print("상행")
                    # print("updnLine : "+rlist['updnLine'])
                    # print("updnLine type : "+str(type(rlist['updnLine'])))

                    if eq(rlist['updnLine'],'상행') or eq(rlist['updnLine'],'외선'):
                        #print("방향 일치")
                        arrivalData = rlist
                        break
                else:
                    # print("하행")
                    # print("updnLine : "+rlist['updnLine'])
                    # print("updnLine type : "+str(type(rlist['updnLine'])))

                    if eq(rlist['updnLine'],'하행') or eq(rlist['updnLine'],'내선'):
                        #print("방향 일치")
                        arrivalData = rlist
                        break
        # print("arrival Data : "+str(arrivalData))
        # print("arrival Data type : "+str(type(arrivalData)))
        if not arrivalData:
            print("none!!")
            return "none","none"
        print("지하철이 어디에 있을까???"+arrivalData['arvlMsg2'])
        return arrivalData['arvlMsg2'],arrivalData['trainLineNm']
    except urllib.error.HTTPError:
        print("error!!")
        return "error","error"
    #
    #         if eq(list['subwayId'], laneID) and list['updnLine']==direction:
    #             if list['arvlMsg2'] == "전역 도착" or list['arvlMsg2'] == "전역 출발":
    #                 return idx+1
    #             elif "[" in list['arvlMsg2']:#[5]번째 전역 (화전)
    #                 info_str = list['arvlMsg2'].split()
    #                 info_str2 = info_str[2]
    #                 info_str2 = info_str2[1:len(info_str2)-1]
    #
    #                 new_data = getStationInfo(info_str2)
    #                 new_station_info = new_data['result']['station']
    #                 new_stationID = 0
    #
    #                 for idx, info in enumerate(new_station_info):
    #                     if line_number in info['laneName']:
    #                         new_stationID = int(new_data['result']['station'][idx]['stationID'])
    #
    #                 if eq(direction,"상행") or eq(direction,"외선"):
    #                     return 6-(new_stationID-cID)
    #                 elif eq(direction,"하행") or eq(direction,"내선"):
    #                     return cID-new_stationID
    #             elif "(" in list['arvlMsg2']:#3분 58초 후 (삼각지)
    #                 my_str = list['arvlMsg2'].split()
    #                 for idx,i in enumerate(my_str):
    #                     if "(" in i:
    #                         my_str2 = my_str[idx]
    #
    #                 my_str2 = my_str2[1:len(my_str2)-1]
    #                 new_data = getStationInfo(my_str2)
    #                 new_station_info = new_data['result']['station']
    #                 new_stationID = 0
    #
    #                 for idx, info in enumerate(new_station_info):
    #                     if line_number in info['laneName']:
    #                         new_stationID = int(new_data['result']['station'][idx]['stationID'])
    #
    #                 if eq(direction,"상행") or eq(direction,"외선"):
    #                     return 6-(new_stationID-cID)
    #                 elif eq(direction,"하행") or eq(direction,"내선"):
    #                     return cID-new_stationID
    #             else:
    #                 return idx
    #     return "none"
    # except urllib.error.HTTPError:
    #     return "error"
    # except KeyError:
    #     return "error"
# def get_subway_line(subway_station):
#     ##지하철 호선 리스트
#     my = "f/WM8od4VAXdGg4Q5ZaWSlJ8tIbSpw+nJ4WQ4AFRpsM"
#     encMy = urllib.parse.quote_plus(my)
#     encST = urllib.parse.quote_plus(subway_station)
#
#     odUrl = "https://api.odsay.com/v1/api/searchStation?lang=&stationName="+encST+"&CID=1000&stationClass=2&apiKey="+encMy
#
#     request = urllib.request.Request(odUrl)
#     response = urllib.request.urlopen(request)
#
#     json_rt = response.read().decode('utf-8')
#     data = json.loads(json_rt)
#
#     sub_line_list = []
#     stInfo = data['result']['station']
#
#     for i in stInfo:
#         if i['laneName'] not in sub_line_list:
#             sub_line_list.append(i['laneName'])
#
#     action = 1
#     re = "호선을 선택해 주세요." + "\n"
#     for i in range(0,len(sub_line_list)):
#         re += str(i+1) +". " + sub_line_list[i] + "\n"
#
#     return [re,action,sub_line_list]


# def get_option(stationName):
#
#     SNList = [["반포역", "신반포역", "구반포역"], ["논현역", "신논현역"]]
#
#     print("입력한 역이름 :"+stationName)
#     for e in SNList:
#         #print("e = "+str(e))
#         #print("stationName="+stationName+" line_number="+line_number+" direction="+direction)
#         if stationName in e:
#             #print("리스트에 있음")
#             #print("리스트 길이 : "+str(len(SNList)))
#             for i in range(0, len(SNList)):
#                 #print(str(i)+"번째 리스트 내용 :"+str(SNList[i]))
#                 if stationName in SNList[i]:
#                     option = SNList[i]
#                     #print("option = "+str(option))
#     print("선택사항 : "+str(option))
#
#     return option
