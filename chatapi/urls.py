from django.urls import path
from . import views


urlpatterns = [
	path("chat/",views.ChatView.as_view(),name="Chat_view"),
	path("register/",views.RegisterView.as_view(),name="Register_View"),
	path("login/",views.LoginView.as_view(),name="login_view"),
	path("token/",views.TokenView.as_view(),name="Token_View")
]