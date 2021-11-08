from django.contrib import admin
from django.urls import path
from myapp.views import Webhook, GHLWebhook

urlpatterns = [
    path('', Webhook.as_view()),
    path('twilead', GHLWebhook.as_view()),
]
