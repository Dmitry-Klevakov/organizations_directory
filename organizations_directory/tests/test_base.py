from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ClientAuthentication(APITestCase):
    """
    Класс для аутентификации клиента.
    """

    def set_up_auth(self, is_admin=False):
        user_class = get_user_model()
        self.user = user_class.objects.create(
            username='lauren', password='secret', is_staff=is_admin, is_active=True
        )
        self.api_client = APIClient()
        self.api_client.login(
            username=self.user.username, password=self.user.password
        )
        self.token = self.get_refresh_token()
        jwt = self.get_tokens_for_user()
        self.api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt['access'])

    def get_refresh_token(self):
        """
        Возвращает JWT для пользователя.

        :return: RefreshToken
        """

        return RefreshToken.for_user(self.user)

    def get_tokens_for_user(self):
        """
        Возвращает jwt токены (refresh и access) для указанного клиента.

        :return: токены:
        {
            'refresh': 'LCJhbGciOiJIUzI1NiJ9.eyJ0b290eXBlIiYWNjZXNzIiwZXhwIjxNjI1...',
            'access': 'kiOiJiMzZlYzk4N2RjMWU0MTdjOGIzMjE0MzUyZTg4MjI1YSIsImNsaWV...',
        }
        """

        return {
            'refresh': str(self.token),
            'access': str(self.token.access_token),
        }
