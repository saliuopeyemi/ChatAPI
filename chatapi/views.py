from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import bot


chatbot = bot.Chatbot()
class TestView(APIView):
	def get(self, request):
		test_message = "Tell me something about hitler"
		answer = chatbot.reply(test_message)
		return Response({"result":answer},status=status.HTTP_200_OK)