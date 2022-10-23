from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from organizations_directory.models import Category, Offer, Organization, Product


class ProductSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        """
        Преобразует полученный объект для передачи в теле ответа.

        :param obj: объект Product
        :return: словарь данных продукта
        """

        return {
            'id': obj.id,
            'name': obj.name,
            'category': {
                'id': obj.category.id,
                'name': obj.category.name,
            },
            'offers': [
                {
                    'organization_id': offer.organization_id,
                    'price': offer.price,
                }
                for offer in obj.offer_set.all()
            ],
        }

    def to_internal_value(self, data):
        """
        Вызывается для преобразования примитивного типа данных в его
        внутреннее представление Python. Вызвывает serializers.ValidationError,
        если данные недействительны.
        """

        try:
            name = data['name']
            category_id = data['category_id']
            category = Category.objects.get(id=category_id)
        except KeyError:
            raise serializers.ValidationError(f'Category is a required field.')
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Category object does not exist.')

        try:
            offers_count = Organization.objects.filter(
                id__in=[offer['organization_id'] for offer in data['offers']]
            ).count()
            if offers_count != len(data['offers']):
                raise ObjectDoesNotExist
            offers = [
                {
                    'organization_id': offer['organization_id'],
                    'price': offer.get('price', None)
                } for offer in data['offers']
            ]
        except KeyError:
            raise serializers.ValidationError('organization_id is a required field.')
        except ObjectDoesNotExist:
            raise serializers.ValidationError('Organization object does not exist.')

        return {"name": name, "category": category, "organizations": offers}

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'organizations']

    def create(self, validated_data):
        """
        Создает объект Product, а также связанные объекты Offer.

        :param validated_data: проверенные входящие данные
        :return: объект Product
        """

        organizations = validated_data.pop('organizations')
        product = Product.objects.create(**validated_data)

        for offer in organizations:
            Offer.objects.create(**{**offer, 'product': product})
        return product


class OrganizationSerializer(serializers.ModelSerializer):
    """
    awdad
    """

    class Meta:
        model = Organization
        fields = ['id', 'name', 'description', 'network', 'districts', 'get_offers']
        depth = 1

