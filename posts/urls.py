from django.conf.urls import url
from django.contrib import admin

from .views import (
	posts_list,
	posts_create,
	posts_detail,
	posts_update,
	posts_delete,
	send_newsletter
	)

urlpatterns = [
    url(r'^$',posts_list, name='list'),
    url(r'^create/$',posts_create ),
    url(r'^(?P<slug>[\w-]+)/$',posts_detail, name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$',posts_update, name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$',posts_delete ),
    url(r'^(?P<slug>[\w-]+)/newsletter/$',send_newsletter ),
]

