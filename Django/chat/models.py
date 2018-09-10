from django.db import models
from jsonfield import JSONField

class allData(models.Model):
	session_id = models.CharField(max_length=128,primary_key=True)
	session_end = models.IntegerField(default=0)
	jsondata = models.TextField()
	dialogflow_action = models.IntegerField(default=0)
	bus_action = models.IntegerField(default=0)
	bus_station_result = models.TextField()
	bus_selected = models.TextField(max_length=128)
	bus_arsid = models.TextField()
	subway_action = models.IntegerField(default=0)
	subway_station_result = models.TextField(default="")
	subway_selected = models.TextField(max_length=128,default="")
	subway_station_name = models.TextField(default="")
	diff_path = models.IntegerField(default=0)
	limit_time = models.TextField(default="")


	def __str__(self):
		return self.data
