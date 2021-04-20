from django.db.models import query
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from equity_data.serializers import EquityDataSerializer
from equity_data.models import EquityData

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator

from django.core.cache import cache

# CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class EquityDataViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EquityData.objects.all()
    serializer_class = EquityDataSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('code' , 'name')

    # @method_decorator(cache_page(CACHE_TTL))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class EquityList(viewsets.ViewSet):
    serializer_class = EquityDataSerializer

    def list(self, request):
        keys_to_search = "STDATA:*:*"
        name = request.query_params.get("s")
        page = request.query_params.get("page")
        if name is not None and not name == "":
            keys_to_search = "STDATA:*:*" + str(name).upper() + "*"
        else:
            if page is not None:
                try:
                    page = int(page)
                    page_str = str(page-1)
                    if page == 1:
                        page_str = ""
                    keys_to_search = "STDATA:" + page_str +"[0-9]:*"
                except:
                    pass
        keys = cache.keys(keys_to_search)
        queryset = [cache.get(key) for key in keys]
        print("Result :: " , keys_to_search)
        print("Result :: " , keys[:3])
        print("Result :: " , queryset[:3])
        serializer = EquityDataSerializer(data = queryset , many=True)
        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=400)