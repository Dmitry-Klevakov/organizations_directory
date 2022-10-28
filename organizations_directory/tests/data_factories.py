import random

import factory
from faker.providers import BaseProvider

from organizations_directory.models import *


class CustomProvider(BaseProvider):
    @staticmethod
    def district_name():
        return random.choice(
            ['Советский', 'Железнодорожный', 'Ленинский', 'Октябрьский']
        )

    @staticmethod
    def network_name():
        return random.choice(
            [
                'Тандер',
                'X5',
                'VipAvto',
                'SultanSpa',
                'Индустрия гостеприимства',
                'Zara',
            ]
        )

    @staticmethod
    def category_name():
        return random.choice(
            [
                'Без категории',
                'Хозяйственные товары',
                'Услуги автомастерских',
                'Одежда',
                'Индустрия гостеприимства',
                'Здоровье',
                'Продукты',
            ]
        )

    @staticmethod
    def organization_name():
        return random.choice(
            [
                'Магнит',
                'Пятерочка',
                'Шинный Айболит',
                'Морская звезда',
                'Меридиан',
                'Пенное',
                'ВкусноПицца',
                'Кулибины',
                'Банный двор',
                'Круглосуточный',
                'ZARA',
            ]
        )

    @staticmethod
    def product_name():
        return random.choice(
            [
                'Пиво',
                'Комната',
                'Пицца',
                'Массаж',
                'Колбаса',
                'Ремонт пробитой резины',
                'Чупа-чупс',
                'Рубашка',
                'Сахар',
                'Хлеб',
                'Бассейн',
                'Массаж шеи',
                'Ремонт ходовой',
                'Молоко',
                'Соль',
                'Баня',
            ]
        )

    @staticmethod
    def price():
        return random.choice([10, 50, 32.5, 500, 1000])


factory.Faker.add_provider(CustomProvider)


class DistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = District

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('district_name')


class NetworkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Network

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('network_name')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('category_name')


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('organization_name')
    description = 'Описание организации'
    network = factory.SubFactory(NetworkFactory)
    districts = factory.SubFactory(DistrictFactory)

    @factory.post_generation
    def districts(self, create, extracted, **kwargs):
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        # Add the iterable of groups using bulk addition
        self.districts.add(*extracted)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('product_name')
    category = factory.SubFactory(CategoryFactory)


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Offer

    id = factory.Sequence(lambda n: n)
    product = factory.SubFactory(ProductFactory)
    organization = factory.SubFactory(OrganizationFactory)
    price = factory.Faker('price')
