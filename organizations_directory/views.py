from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from organizations_directory.models import Organization, Product
from organizations_directory.permissions import IsAdminOrIsAuthenticated
from organizations_directory.serializers import OrganizationSerializer, \
    ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    Обработка действий с продуктами/услугами.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAdminOrIsAuthenticated]


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    Обработка действий с предприятиями.
    """

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    http_method_names = ['get']

    @action(methods=['get'], detail=True, url_path='districts')
    def get_organizations_by_district(self, request, pk=None):
        """
        Возвращает список заведений с фильтрацией по району города,
        минимальной/максимальной цене, категории товара, названию товара.
        """

        queryset = self.queryset.prefetch_related('districts').filter(districts=pk)

        min_price = self.request.query_params.get('min_price')
        if min_price:
            queryset = queryset.filter(offer__price=min_price)

        max_price = self.request.query_params.get('max_price')
        if max_price:
            queryset = queryset.prefetch_related('offer_set').filter(
                offer__price=max_price
            )

        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.prefetch_related(
                'offer_set__product__category'
            ).filter(product__category__name=category)

        product_name = self.request.query_params.get('product_name')
        if product_name:
            queryset = queryset.filter(product__name=product_name).defer(
                'product__name'
            )

        data = self.serializer_class(queryset, many=True).data
        return Response(status=200, data=data) if data else Response(status=404)
