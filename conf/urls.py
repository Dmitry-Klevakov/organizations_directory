from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from organizations_directory.views import ProductViewSet, OrganizationViewSet

admin.site.site_header = 'Справочник Организаций'
admin.site.index_title = 'Администрирование базы'

router = SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'organizations', OrganizationViewSet)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api/v1/', include(router.urls)),
]
