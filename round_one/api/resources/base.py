import copy
from random import choice

from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.core.urlresolvers import reverse
from django.utils import translation, datastructures

from tastypie import authentication
from tastypie import authorization
from tastypie import fields
from tastypie import http
from tastypie.bundle import Bundle
from tastypie.http import HttpBadRequest, HttpForbidden, HttpNotFound, HttpCreated, HttpNoContent
from tastypie.exceptions import NotFound
from tastypie.paginator import Paginator
from tastypie.resources import Resource, ModelResource as BaseModelResource, ALL_WITH_RELATIONS, ALL
from tastypie.utils import trailing_slash



class AttrDict(object):
    """
    Allows you to access the keys of a dictionary
    as if they were attributes of an object.
    """
    def __init__(self, *args, **kwargs):
        # Get the kwargs from the first argument..
        # this is because python is quite retarded and
        # won't allow kwargs to have unicode keys.
        if len(args) == 1 and hasattr(args[0], 'keys'):
            kwargs.update(args[0])


        self._dict = {}
        for key, val in kwargs.items():
            self._dict[str(key)] = val

        self.__dict__.update(self._dict)
        super(AttrDict, self).__init__()

    def to_dict(self):
        return self._dict



class JSONField(fields.ApiField):

    def convert(self, value):
        return value



class NoCountPaginator(Paginator):
    """
    Paginator that turns off the default counting
    """
    def get_count(self):
        """
        Returns a count of the total number of objects seen.
        """
        return 0



class DjangoAuthentication(authentication.Authentication):
    """
    Basic django authentication
    """
    def is_authenticated(self, request, **kwargs):
        return request.user.is_authenticated()

    # Optional but recommended
    def get_identifier(self, request):
        return request.user.username



class ModelResource(BaseModelResource):
    """
    Base model resource
    """
    pass


class Resource(Resource):
    """
    Base resource
    """
    def __init__(self, *args, **kwargs):
        super(Resource, self).__init__(*args, **kwargs)
        self._meta.paginator_class = NoCountPaginator  # Hokey-pokey

    def _get_offset(self, bundle):
        """
        Returns the correct offset
        """
        page = int(bundle.request.GET.get('page', '1'))
        return int(bundle.request.GET.get('offset', '0')) or (page - 1) * 10

    def alter_list_data_to_serialize(self, request, to_be_serialized):
        if to_be_serialized:
            return to_be_serialized.get('objects', [])
        else:
            return to_be_serialized

    def get_list(self, request, **kwargs):
        """
        get_list
        """
        try:
            resp = super(Resource, self).get_list(request, **kwargs)
        except ObjectDoesNotExist:
            return HttpNotFound()
        return resp
