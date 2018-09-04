from django.db import models
from jsonfield import JSONField

class preData(models.Model):
	user = models.CharField(max_length=128, primary_key=True)
	msg = models.CharField(max_length=128)

	def __str__(self):
		return self.msg

# Create your models here.
