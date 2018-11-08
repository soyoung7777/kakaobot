import json
import urllib.request
import urllib.parse
from operator import eq
from collections import OrderedDict

def main():
	
	my = "2Y3C1Vf5IqtpTOyTtlHh1zhP2SJSByC9xqsjCDo/4FQ"
	encMy = urllib.parse.quote_plus(my)

	stID = ""

	idList = {"11421","11422","11423","11424","11425","11427","11428","11429","11430","11431","11432","11433"}
			
	ordList = OrderedDict()
	satList = OrderedDict()
	sunList = OrderedDict()
	nameList = OrderedDict()

	for stID in idList:
		encID = urllib.parse.quote_plus(stID)
	
		ordTime = OrderedDict()
		satTime = OrderedDict()
		sunTime = OrderedDict()
	
		odUrl_u = "https://api.odsay.com/v1/api/subwayTimeTable?1ang=0&stationID="+encID+"&wayCode=1&showExpressTime=1&apiKey="+encMy

		request = urllib.request.Request(odUrl_u)
		response = urllib.request.urlopen(request)

		real_json = json.loads(response.read().decode('utf-8'))
	
		key = str(real_json['result']['stationName'])
		print(key)
		nameList[stID] = key
		
		try:
			ordTime["up"] = real_json['result']['OrdList']['up']['time']
			satTime["up"] = real_json['result']['SatList']['up']['time']
			sunTime["up"] = real_json['result']['SunList']['up']['time']
		except:
			print("up data is not exist")
		
	
		odUrl_d = "https://api.odsay.com/v1/api/subwayTimeTable?1ang=0&stationID="+encID+"&wayCode=2&showExpressTime=1&apiKey="+encMy
		
		request = urllib.request.Request(odUrl_d)
		response = urllib.request.urlopen(request)
		
		real_json = json.loads(response.read().decode('utf-8'))
	
		try :
			ordTime["down"] = real_json['result']['OrdList']['down']['time']
			satTime["down"] = real_json['result']['SatList']['down']['time']
			sunTime["down"] = real_json['result']['SunList']['down']['time']
		except:
			print("down data is not exist")
		
	
		ordList[key] = ordTime
		satList[key] = satTime
		sunList[key] = sunTime
		print("success")

	with open('name_lane_서해.json', 'w', encoding="utf-8") as make_file:
		json.dump(nameList,make_file, ensure_ascii=False, indent="\t")

	with open('ord_lane_서해.json', 'w', encoding="utf-8") as make_file:
		json.dump(ordList,make_file, ensure_ascii=False, indent="\t")

	with open('sat_lane_서해.json', 'w', encoding="utf-8") as make_file:
		json.dump(satList,make_file, ensure_ascii=False, indent="\t")
	
	with open('sun_lane_서해.json', 'w', encoding="utf-8") as make_file:
		json.dump(sunList,make_file, ensure_ascii=False, indent="\t")

	print("aaa\n")

if __name__ == '__main__':
	main()
