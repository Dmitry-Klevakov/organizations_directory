from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, \
    TokenVerifyView

from organizations_directory.views import OrganizationViewSet, ProductViewSet

admin.site.site_header = 'Справочник Организаций'
admin.site.index_title = 'Администрирование базы'

router = SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'organizations', OrganizationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(router.urls)),
    path(
        'api/v1/token/create/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair',
    ),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
