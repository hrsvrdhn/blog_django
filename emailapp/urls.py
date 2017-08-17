from django.conf.urls import url
from django.contrib import admin

from .views import (
	# subscribe,
	confirmMail,
	UnSubscribe,
	)

urlpatterns = [
    # url(r'^$',subscribe, name='subscribe'),
    url(r'confirm/(?P<key>[\w-]+)/$',confirmMail, name="confirm"),
    url(r'unsubscribe/(?P<key>[\w-]+)/$',UnSubscribe, name="unsubscribe"),
]
