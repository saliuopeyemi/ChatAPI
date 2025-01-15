from django.shortcuts import render
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models
from . import bot
from . import serializers


chatbot = bot.Chatbot()
class ChatView(APIView):
	serializer_class = serializers.ChatSerializer
	permission_classes = [
		IsAuthenticated,
	]
	def post(self,request):
		serializer = self.serializer_class(data=request.data,context = {"request":request})
		if serializer.is_valid(raise_exception=True):
			reply = serializer.save()
			return Response({"Bot":reply},status=status.HTTP_200_OK)

	def get(self,request):
		user_id = request.user.id
		chat_history = models.Chat.objects.filter(user_id=user_id).order_by("time_stamp")
		container = []
		for item in chat_history.values():
			data = {f"{request.user}: {item['message']}":f"Bot: {item['response']}"}
			container.append(data)
		return Response({"Chat History":container},status=status.HTTP_200_OK)

class RegisterView(APIView):
	permission_classes = [AllowAny,]
	serializer_class=serializers.UserSerializer
	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		if serializer.is_valid(raise_exception=True):
			output =serializer.save()
			return Response({"Status":f"{output.username} created successfully"})

class LoginView(APIView):
	permission_classes=[
		AllowAny
	]
	serializer_class = serializers.LoginSerializer
	def post(self,request):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data
		token = RefreshToken.for_user(user)
		return Response(
		                {
		                "refresh":str(token),
		                "access":str(token.access_token)
		                })

class TokenView(APIView):
	permission_classes=[IsAuthenticated]
	def get(self,request):
		user_id = request.user.id
		available_tokens= models.UserExtend.objects.get(id_id=user_id).tokens
		return Response({"Available Token":available_tokens},status=status.HTTP_200_OK)