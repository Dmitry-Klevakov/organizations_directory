from django.db.models import Max, Min
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from organizations_directory.models import Organization, Product
from organizations_directory.serializers import OrganizationSerializer, \
    ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Обработка действий с продуктами/услугами.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Возвращает список заведений и детальную информацию по заведению.
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    http_method_names = ['get']


class OrganizationByDistrictViewSet(viewsets.ModelViewSet):
    """
    Возвращает список заведений с фильтрацией по району города,
    минимальной/максимальной цене, категории товара и посиком по названию товара.
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    http_method_names = ['get']
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['product__category__name']
    search_fields = ['product__name']

    def get_queryset(self):
        self.queryset = self.queryset.filter(districts=self.kwargs.pop('pk'))
        min_price = self.request.query_params.get('min_price')
        if min_price:
            self.queryset = self.queryset.annotate(
                min_price=Min('offer__price')
            ).filter(min_price=min_price)

        max_price = self.request.query_params.get('max_price')
        if max_price:
            self.queryset = self.queryset.annotate(
                max_price=Max('offer__price')
            ).filter(max_price=max_price)
        return self.queryset
