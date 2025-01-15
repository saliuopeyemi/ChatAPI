from rest_framework import serializers
from . import bot
from . import models
from django.contrib.auth.models import User
import re

chatbot = bot.Chatbot()



class ChatSerializer(serializers.Serializer):
	text = serializers.CharField(max_length=999999999999999999)

	def validate(self,data):
		request = self.context["request"]
		user_id = request.user.id
		data["id"] = user_id
		available_token = models.UserExtend.objects.get(id_id=user_id).tokens
		if available_token < 100:
			raise serializers.ValidationError("Insufficient Token")
		else:
			return data

	def create(self,validated_data):
		text = validated_data["text"]
		text_treated = re.sub('"',"",text)
		reply = chatbot.reply(str(text_treated))
		models.Chat.objects.create(user_id=validated_data["id"],message=text,response=reply)
		available_token = models.UserExtend.objects.get(id_id=validated_data["id"]).tokens
		models.UserExtend.objects.filter(id_id=validated_data["id"]).update(tokens=available_token-100)
		return reply

class UserSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=50)
	email = serializers.CharField(max_length=200)
	password= serializers.CharField(max_length=128)
	password_confirm = serializers.CharField(max_length=128)

	def validate_email(self,value):
		user = User.objects.filter(email=value)
		if user.exists():
			raise serializers.ValidationError("Existing Email!")
		else:
			if "@" not in value:
				raise serializers.ValidationError("Invalid Email!")
			else:
				return value

	def validate_username(self,value):
		user = User.objects.filter(username=value)
		if user.exists():
			raise serializers.ValidationError("Existing Username!")
		else:
				return value

	def validate(self,data):
		username= data["username"]
		email = data["email"]
		password_1 = data["password"]
		password_2 = data["password_confirm"]
		if password_1 == password_2:
			return data
		else:
			raise serializers.ValidationError("Unmatched Passwords")

	def create(self,validated_data):
		user = User.objects.create(
		                                  username=validated_data["username"],
		                                  email = validated_data["email"],
		                                  password = validated_data["password"]
		                                  )
		models.UserExtend.objects.create(id_id=user.id,tokens=4000)
		return user

class LoginSerializer(serializers.Serializer):
	username = serializers.CharField(max_length=250)
	password = serializers.CharField(max_length=250)

	def validate(self,data):
		try:
			user = User.objects.get(username=data["username"])
			if user and (data["password"] == user.password):
				return user
			else:
				raise serializers.ValidationError("Invalid Credentials!")
		except:
			raise serializers.ValidationError("Invalid Credentials!")
		