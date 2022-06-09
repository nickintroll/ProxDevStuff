from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
	re_path(
		r'ws/ch/room/(?P<slug>\d+)/$', ChatConsumer
	),
]