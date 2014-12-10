import logging

from django.conf import settings
from django.conf.urls import *
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse

from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized, HttpBadRequest, HttpForbidden
from tastypie.resources import ALL_WITH_RELATIONS
from tastypie.utils import trailing_slash


from .base import Resource, DjangoAuthentication

log = logging.getLogger(__name__)



class UserResource(Resource):
    """
    User Resource
    """
    data = fields.DictField(attribute='data')

    def override_urls(self):
        return [
            url(r"^account%s$" % (trailing_slash()), self.wrap_view('dispatch_detail'), name="api_account_detail"),
        ]

    def obj_get(self, bundle, **kwargs):
        profile = Profile.get(bundle.request.user)
        return profile

    class Meta:
        resource_name = 'account'
        detail_allowed_methods = ['get']
