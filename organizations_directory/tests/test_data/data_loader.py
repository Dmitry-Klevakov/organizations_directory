import os

import yaml
from django.conf import settings


class BaseYamlTestDataLoader:
    """
    Базовый класс для загрузки тестовых данных из yml-файлов.
    """

    # Имена файлов в формате:
    # {'name': '/file_path.yml'}
    test_data_files = None

    @classmethod
    def load_test_data(cls):
        """
        Выполняет загрузку тестовых данных из yml-файлов.

        :return: тестовые данные
        """

        result = {}
        for name, file_path in cls.test_data_files.items():
            test_data_file = os.path.join(settings.BASE_DIR, file_path)
            with open(test_data_file, 'r') as stub_file:
                result.update({name: yaml.load(stub_file, Loader=yaml.Loader)})
        return result
