from django.urls import path
from .views import index, set_source, api_chat, clear_history

urlpatterns = [
    path("", index, name="index"),
    path("api/source/", set_source, name="set_source"),
    path("api/chat/", api_chat, name="api_chat"),
    path("api/clear/", clear_history, name="clear_history"),
]