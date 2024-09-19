from functools import cached_property

from puty import purify
from rest_framework.response import Response
from rest_framework.views import APIView

from djackal import query_filter
from djackal.settings import djackal_settings
from djackal.utils import value_mapper


class QueryFilterMixin:
    lookup_map = {}
    extra_map = {}
    ordering_map = {}

    ordering_key = 'ordering'
    ordering_default = None

    filter_schema = {}

    user_field = None
    bind_user_field = None

    def get_lookup_map(self, **additional):
        d = self.lookup_map or dict()
        return {**d, **additional}

    def get_filter_schema(self, **additional):
        d = self.filter_schema or dict()
        return {**d, **additional}

    def get_extra_map(self, **additional):
        d = self.extra_map or dict()
        return {**d, **additional}

    def get_ordering_map(self, **additional):
        d = self.ordering_map or dict()
        return {**d, **additional}

    def get_user_field(self):
        return self.user_field

    def query_by_lookup_map(self, queryset, lookup_map=None):
        if lookup_map is None:
            lookup_map = self.get_lookup_map()

        mapped = value_mapper(lookup_map, self.kwargs)
        return queryset.filter(**mapped)

    def query_by_user(self, queryset, user_field=None):
        if user_field is None:
            user_field = self.get_user_field()

        if not self.has_auth() or not user_field:
            return queryset
        return queryset.filter(**{user_field: self.request.user})

    def query_by_extra_map(self, queryset, extra_map=None):
        if extra_map is None:
            extra_map = self.get_extra_map()
        return queryset.filter(**extra_map)

    def query_by_filter_schema(self, queryset, filter_schema=None):
        params = self.get_query_params_dict()
        if filter_schema is None:
            filter_schema = self.get_filter_schema()

        return query_filter.filtering(queryset, params, filter_schema)

    def query_by_ordering(self, queryset, order_map=None):
        if order_map is None:
            order_map = self.get_ordering_map()

        params = self.get_query_params_dict()
        param_value = params.get(self.ordering_key)

        if order_map is not None:
            order_value = order_map.get(param_value)
        else:
            order_value = param_value

        if not order_value:
            if not self.ordering_default:
                return queryset
            order_value = self.ordering_default

        order_by = order_value.split(',')
        return queryset.order_by(*order_by)

    def get_filtered_queryset(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = self.query_by_user(queryset)
        queryset = self.query_by_lookup_map(queryset)
        queryset = self.query_by_extra_map(queryset)
        queryset = self.query_by_filter_schema(queryset)
        queryset = self.query_by_ordering(queryset)

        return queryset

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        queryset = self.query_by_user(queryset)
        queryset = self.query_by_lookup_map(queryset)
        queryset = self.query_by_extra_map(queryset)

        obj = queryset.first()
        if obj is None:
            return None
        self.check_object_permissions(request=self.request, obj=obj)
        return obj


class PageMixin:
    pagination_class = djackal_settings.DEFAULT_PAGINATION_CLASS
    paging = False

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if not self.paging:
                self._paginator = None
            else:
                if self.pagination_class is None:
                    self._paginator = None
                else:
                    self._paginator = self.pagination_class()
        return self._paginator

    def get_paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_meta(self):
        return self.paginator.get_paginated_meta()


class DataPurifyMixin:
    data_schema = None
    query_params_schema = None

    def get_purified_data(self, key=None, many=False):
        schema = self.get_data_schema(key)
        return purify(self.request.data, schema, many=many)

    @cached_property
    def purified_data(self):
        return self.get_purified_data()

    def get_data_schema(self, key=None):
        if key in self.data_schema:
            return self.data_schema[key]
        return self.data_schema

    def get_purified_query_params(self, key=None, many=False):
        schema = self.get_query_params_schema(key)
        return purify(self.get_query_params_dict(), schema, many=many)

    @cached_property
    def purified_query_params(self):
        return self.get_purified_query_params()

    def get_query_params_schema(self, key=None):
        if key in self.query_params_schema:
            return self.query_params_schema[key]
        return self.query_params_schema


class BaseDjackalAPIView(APIView):
    default_permission_classes = ()
    default_authentication_classes = ()

    result_root = 'result'
    result_meta = 'meta'

    required_auth = False

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def get_default_exception_handler(self):
        return djackal_settings.EXCEPTION_HANDLER

    def get_authentication_classes(self):
        if self.authentication_classes:
            return (
                *self.default_authentication_classes,
                *self.authentication_classes
            )
        return self.default_authentication_classes

    def get_authenticators(self):
        return [auth() for auth in self.get_authentication_classes()]

    def get_permission_classes(self):
        if self.permission_classes:
            return (
                *self.default_permission_classes,
                *self.permission_classes
            )
        return self.default_permission_classes

    def get_permissions(self):
        return [permission() for permission in self.get_permission_classes()]

    def pre_check_object_permissions(self, request, obj):
        pass

    def pre_check_permissions(self, request):
        pass

    def pre_handle_exception(self, exc):
        pass

    def pre_method_call(self, request, *args, **kwargs):
        pass

    def post_check_object_permissions(self, request, obj):
        pass

    def post_check_permissions(self, request):
        pass

    def post_method_call(self, request, response, *args, **kwargs):
        pass

    def check_permissions(self, request):
        self.pre_check_permissions(request)
        super().check_permissions(request)
        self.post_check_permissions(request)

    def check_object_permissions(self, request, obj):
        self.pre_check_object_permissions(request, obj)
        super().check_object_permissions(request, obj)
        self.post_check_object_permissions(request, obj)

    def dispatch(self, request, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers

        try:
            self.initial(request, *args, **kwargs)

            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            self.pre_method_call(request, *args, **kwargs)
            response = handler(request, *args, **kwargs)
            self.post_method_call(request, response, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response

    def handle_exception(self, exc):
        """
        high jacking exception and handle with default_exception_handler
        """
        self.pre_handle_exception(exc)
        djackal_handler = self.get_default_exception_handler()
        context = self.get_exception_handler_context()
        response = djackal_handler(exc, context)
        if response is not None:
            response.exception = True
            return response
        else:
            return super().handle_exception(exc)

    def has_auth(self):
        return self.request.user is not None and self.request.user.is_authenticated

    def get_meta(self, **kwargs):
        return kwargs

    def get_query_params_dict(self):
        result = {}
        for key, value in self.request.query_params.lists():
            if len(value) == 1:
                result[key] = value[0]
            else:
                result[key] = value
        return result

    def simple_response(self, result=None, status=200, meta=None, headers=None, **kwargs):
        response_data = {}

        if self.result_root:
            response_data[self.result_root] = result
            if self.result_meta:
                meta = self.get_meta(**(meta or dict()))
                response_data[self.result_meta] = meta
        else:
            response_data = result or dict()

        return Response(response_data, status=status, headers=headers, **kwargs)


class DjackalAPIView(BaseDjackalAPIView, QueryFilterMixin, PageMixin, DataPurifyMixin):
    model = None
    queryset = None

    bind_kwargs_map = {}

    serializer_class = None

    def get_queryset(self):
        assert self.queryset is not None or self.model is not None, (
            '{} should include a `queryset` or `model` attribute'
            'or override the get_queryset() method'.format(self.__class__.__name__)
        )
        if self.queryset is not None:
            queryset = self.queryset.all()
            return queryset
        else:
            return self.model.objects.all()

    def get_model(self):
        if self.model is not None:
            return self.model
        queryset = self.get_queryset()
        assert queryset is not None, (
            '{} should include a `model` or `queryset` attribute'
            'or override the get_model() method'.format(self.__class__.__name__)
        )
        return queryset.model

    def get_serializer_class(self):
        return self.serializer_class

    def get_serializer_context(self, **kwargs):
        return kwargs

    def get_serializer(self, instance, context=None, many=False, klass=None):
        if klass is None:
            klass = self.get_serializer_class()
        context = self.get_serializer_context(**(context or dict()))
        ser = klass(instance, many=many, context=context)
        return ser

    def get_bind_kwargs_map(self, **additional):
        d = self.bind_kwargs_map or dict()
        return {**d, **additional}

    def get_bind_kwargs_data(self):
        return value_mapper(self.get_bind_kwargs_map(), self.kwargs)
