from organizations_directory.models import Category, District, Organization
from organizations_directory.tests.data_factories import CategoryFactory, \
    DistrictFactory, NetworkFactory, OfferFactory, OrganizationFactory, \
    ProductFactory
from organizations_directory.tests.test_base import ClientAuthentication
from organizations_directory.tests.test_data.data_loader import \
    BaseYamlTestDataLoader


class TestProductViewSet(BaseYamlTestDataLoader, ClientAuthentication):
    BASE_URL = '/api/v1/organizations/'
    test_data_files = {'all': 'organizations_directory/tests/test_data/products.yml'}

    def setUp(self) -> None:
        self.test_data = self.load_test_data()['all']
        self.prepare_data_for_test()
        self.set_up_auth()

    @staticmethod
    def prepare_data_for_test():
        first_category = CategoryFactory(name='Продукты питания')
        first_product = ProductFactory(name='Молоко', category=first_category)
        second_product = ProductFactory(name='Хлеб', category=first_category)
        first_district = DistrictFactory(id=1, name='Советский')
        second_district = DistrictFactory(id=2, name='Железнодорожный')
        first_network = NetworkFactory(id=1, name='Тандер')
        second_network = NetworkFactory(id=2, name='X5')
        first_organization = OrganizationFactory.create(
            id=1,
            name='Магнит',
            network=first_network,
            districts=(first_district, second_district),
        )
        second_organization = OrganizationFactory.create(
            id=2,
            name='Пятерочка',
            network=second_network,
            districts=(first_district,),
        )
        OfferFactory(
            product=first_product, organization=first_organization, price=50.5
        )
        OfferFactory(
            product=first_product, organization=second_organization, price=55
        )
        OfferFactory(
            product=second_product, organization=first_organization, price=30
        )
        OfferFactory(
            product=second_product, organization=second_organization, price=33
        )

    def test_get_detail_info_about_organization(self):
        """
        Тест проверяет работу api по возврату детальной информации о предприятии.

        Ожидаемый результат:
        - статус ответа 200
        - возвращаемое значение совпадает с ожидаемым.
        """

        response = self.api_client.get(
            self.BASE_URL + '1/', content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data, self.test_data['organization_expected_value']
        )

    def test_organizations_by_districts(self):
        """
        Тест проверяет работу api по возврату информации
        о предприятих переданного района.

        Ожидаемый результат:
        - статус ответа 200
        - возвращаемое значение совпадает с ожидаемым.
        """

        response = self.api_client.get(
            self.BASE_URL + 'districts/1/', content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            self.test_data['organizations_by_district_expected_value'],
        )

    def test_organizations_with_filter_by_product_category(self):
        """
        Тест проверяет работу api по возврату информации
        о предприятих переданного района c применением фильтрации
        по категории товара.

        Ожидаемый результат:
        - статус ответа 200
        - возвращаемое значение совпадает с ожидаемым.
        """

        district_id = 1

        category = CategoryFactory(name='Хозтовары')
        product = ProductFactory(name='Мыло', category=category)
        network = NetworkFactory(id=3, name='Сеть хозяйственных магазинов')
        organization = OrganizationFactory.create(
            id=3,
            name='Мойдодыр',
            network=network,
            districts=(District.objects.get(id=district_id),),
        )
        OfferFactory(product=product, organization=organization, price=25.3)

        response = self.api_client.get(
            self.BASE_URL
            + f'districts/{district_id}/?product__category__name={category.name}',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            self.test_data['filter_by_product_category_name_expected_value'],
        )

    def test_organizations_with_filter_by_min_price(self):
        """
        Тест проверяет работу api по возврату информации
        о предприятих переданного района c применением фильтрации
        минимальной цене на товары предприятия.

        Ожидаемый результат:
        - статус ответа 200
        - возвращаемое значение совпадает с ожидаемым.
        """

        district_id = 1
        price = 5

        product = ProductFactory(
            name='Чупа-чупс', category=Category.objects.get(name='Продукты питания')
        )
        OfferFactory(
            product=product,
            organization=Organization.objects.get(name='Пятерочка'),
            price=price,
        )

        response = self.api_client.get(
            self.BASE_URL + f'districts/{district_id}/?min_price={price}',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            self.test_data['filter_by_min_price_expected_value'],
        )

    def test_organizations_with_filter_by_max_price(self):
        """
        Тест проверяет работу api по возврату информации
        о предприятих переданного района c применением фильтрации
        минимальной цене на товары предприятия.

        Ожидаемый результат:
        - статус ответа 200
        - возвращаемое значение совпадает с ожидаемым.
        """

        district_id = 1
        price = 800

        product = ProductFactory(
            name='Nutella', category=Category.objects.get(name='Продукты питания')
        )
        OfferFactory(
            product=product,
            organization=Organization.objects.get(name='Пятерочка'),
            price=price,
        )

        response = self.api_client.get(
            self.BASE_URL + f'districts/{district_id}/?max_price={price}',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0],
            self.test_data['filter_by_max_price_expected_value'][1],
        )

        OfferFactory(
            product=product,
            organization=Organization.objects.get(name='Магнит'),
            price=price,
        )

        response = self.api_client.get(
            self.BASE_URL + f'districts/{district_id}/?max_price={price}',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            self.test_data['filter_by_max_price_expected_value'],
        )

    def test_search_by_product_name(self):
        """
        Тест проверяет работу api по возврату информации
        о предприятии переданного района c применением посика по названию продукта.

        Ожидаемый результат:
        - статус ответа 200
        - возвращаемое значение совпадает с ожидаемым.
        """

        district_id = 1
        price = 800

        product = ProductFactory(
            name='Nutella', category=Category.objects.get(name='Продукты питания')
        )
        OfferFactory(
            product=product,
            organization=Organization.objects.get(name='Пятерочка'),
            price=price,
        )

        response = self.api_client.get(
            self.BASE_URL + f'districts/{district_id}/?search={product.name[2:5]}',
            content_type='application/json',
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data[0],
            self.test_data['filter_by_max_price_expected_value'][1],
        )
