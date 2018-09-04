from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from chat.models import preData

def keyboard(request):
	return JsonResponse({
		'type' : 'text'
	})

@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))

	msg = json.loads(message)

	cont_str = msg['content']
	user_str = msg['user_key']

	txt = cont_str + "\n###\n" + user_str
	
	#insert
	#preData(user=user_str, msg=cont_str).save()
	
	result = preData.objects.filter(user=user_str)[0]
	pData = result.msg

	txt += "\n\n\npre -> \n"+pData


	return JsonResponse({
		'message':{'text':"!!!\n\n"+txt+"\n\n!!!"},
		'keyboard':{'type':'text'}
		})


