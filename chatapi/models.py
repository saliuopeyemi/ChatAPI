from django.db import models
from django.contrib.auth.models import User

class UserExtend(models.Model):
	id = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
	tokens = models.IntegerField(default=4000)

class Chat(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	message = models.TextField()
	response = models.TextField()
	time_stamp = models.DateTimeField(auto_now_add=True)
