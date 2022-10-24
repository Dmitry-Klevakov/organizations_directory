from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, \
    TokenVerifyView

from organizations_directory.views import OrganizationByDistrictViewSet, \
    OrganizationViewSet, ProductViewSet


admin.site.site_header = 'Справочник Организаций'
admin.site.index_title = 'Администрирование базы'

router = SimpleRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'organizations', OrganizationViewSet, basename='organization')


urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/organizations/districts/<int:pk>/',
        OrganizationByDistrictViewSet.as_view({'get': 'list'}),
        name='organizations_by_district',
    ),
    path(
        'api/v1/token/create/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Organizations directory",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email="klevakov_de@mail.ru"),
        license=openapi.License(name='BSD 2-Clause "Simplified" License'),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

swagger_urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    re_path(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]

urlpatterns += swagger_urlpatterns
