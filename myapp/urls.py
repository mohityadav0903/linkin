from django.contrib import admin
from django.urls import path
from myapp.views import Webhook

urlpatterns = [
    path('', Webhook.as_view()),
]
