from django.contrib import admin
from django.urls import path
from myapp.views import Webhook, GHLWebhook,MsgWebhook

urlpatterns = [
    path('', Webhook.as_view()),
    path('twilead', GHLWebhook.as_view()),
    path('msg', MsgWebhook.as_view()),
]
