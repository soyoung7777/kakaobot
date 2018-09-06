from django.db import models
from jsonfield import JSONField

class allData(models.Model):
	session_id = models.CharField(max_length=128,primary_key=True)
	session_end = models.IntegerField(default=0)
	jsondata = models.TextField()
	dialogflow_action = models.IntegerField(default=0)
	bus_action = models.IntegerField(default=0)
	bus_station_result = models.IntegerField(default=0)
	bus_selected = models.CharField(max_length=128)
	bus_arsid = models.IntegerField(default=0)


	def __str__(self):
		return self.data
