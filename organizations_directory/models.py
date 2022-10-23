from django.db import models


class District(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование района')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Район города'
        verbose_name_plural = 'Районы города'


class Network(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование сети')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Сеть предприятий'
        verbose_name_plural = 'Сети предприятий'


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование категории')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'


class Organization(models.Model):
    name = models.CharField(max_length=50, verbose_name='Наименование предприятия')
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    network = models.ForeignKey(
        Network,
        on_delete=models.CASCADE,
        related_name='organizations',
        verbose_name='Сеть предприятий',
    )
    districts = models.ManyToManyField(District)

    def __str__(self):
        return self.name

    def get_offers(self):
        """
        Возвращает список строк с товарами организации и их ценами.

        :return: ['Колбаса - 530.5 руб.', ]
        """

        offers = self.offer_set.only('price', 'product__name')
        return [f'{offer.product.name} - {offer.price} руб.' for offer in offers]

    def get_districts(self):
        """
        Возвращает список районов к которым принадлежит предприятие.

        :return: ['Ленинский', ]
        """

        return list(self.districts.values_list('name', flat=True))

    class Meta:
        ordering = ['id']
        verbose_name = 'Предприятие'
        verbose_name_plural = 'Предприятия'


class Product(models.Model):
    name = models.CharField(
        max_length=50, verbose_name='Наименование товара или услуги'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name='products',
        verbose_name='Категория товара или услуги',
    )
    organizations = models.ManyToManyField(Organization, through='Offer')

    def __str__(self):
        return self.name

    def get_offers(self):
        """
        Возвращает список строк с организациями в котрых представлен товар.

        :return: ['Магнит на Зорге', ]
        """

        offers = (
            Offer.objects.select_related('organization')
            .filter(product_id=self.id)
            .only('price', 'organization__name')
        )
        return [
            f'{offer.organization.name} - {offer.price} руб.' for offer in offers
        ]

    class Meta:
        ordering = ['id']
        verbose_name = 'Товар/Услуга'
        verbose_name_plural = 'Товары/Услуги'


class Offer(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, verbose_name='Продукт/Услуга'
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, verbose_name='Предприятие'
    )
    price = models.FloatField(verbose_name='Цена', blank=True, null=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Предложение'
        verbose_name_plural = 'Предложения'
