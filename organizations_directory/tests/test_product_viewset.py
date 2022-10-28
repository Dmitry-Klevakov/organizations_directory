from organizations_directory.tests.data_factories import CategoryFactory, \
    DistrictFactory, NetworkFactory, OfferFactory, OrganizationFactory, \
    ProductFactory
from organizations_directory.tests.test_base import ClientAuthentication
from organizations_directory.tests.test_data.data_loader import \
    BaseYamlTestDataLoader


class TestProductViewSet(BaseYamlTestDataLoader, ClientAuthentication):
    BASE_URL = '/api/v1/products/'
    test_data_files = {'all': 'organizations_directory/tests/test_data/products.yml'}

    def setUp(self) -> None:
        self.test_data = self.load_test_data()['all']
        self.prepare_data_for_test()

    def prepare_data_for_test(self):
        first_category = CategoryFactory(id=1, name='Продукты питания')
        first_product = ProductFactory(id=1, name='Молоко', category=first_category)
        second_product = ProductFactory(id=2, name='Хлеб', category=first_category)
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

    def test_get_products(self):
        """
        Тест проверяет работу api по возврату детальной информации по товару/услуге.

        Ожидаемый результат:
        - статус ответа 200
        """

        self.set_up_auth()
        response = self.api_client.get(
            self.BASE_URL, content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            list(response.data), self.test_data['products_expected_result']
        )
