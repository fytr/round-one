#coding=utf-8
from django.conf import settings
from django.conf.urls import *
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt

from tastypie.api import Api

from api import resources

v1_api = Api(api_name='1.0')
v1_api.register(resources.UserResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)
