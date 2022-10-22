from django.contrib import admin

from .models import *


@admin.register(District)
class DictrictAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    list_per_page = 5


@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    ordering = ['name']
    list_per_page = 3


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    list_per_page = 10


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'network', 'get_offers', 'get_districts']
    list_editable = ['description', 'network']
    ordering = ['name']
    list_per_page = 5


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'get_offers']
    list_editable = ['category']
    ordering = ['name']
    list_per_page = 10


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'organization', 'price']
    list_editable = ['price']
    ordering = ['product']
    list_per_page = 10
