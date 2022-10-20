# Generated by Django 3.1.14 on 2022-10-22 08:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование категории')),
            ],
            options={
                'verbose_name': 'Категория товара',
                'verbose_name_plural': 'Категории товаров',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование района')),
            ],
            options={
                'verbose_name': 'Район города',
                'verbose_name_plural': 'Районы города',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование сети')),
            ],
            options={
                'verbose_name': 'Сеть предприятий',
                'verbose_name_plural': 'Сети предприятий',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField(blank=True, null=True, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование предприятия')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Описание')),
                ('districts', models.ManyToManyField(to='organizations_directory.District')),
                ('network', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='organizations', to='organizations_directory.network', verbose_name='Сеть предприятий')),
            ],
            options={
                'verbose_name': 'Предприятие',
                'verbose_name_plural': 'Предприятия',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наименование товара или услуги')),
                ('category', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, related_name='products', to='organizations_directory.category', verbose_name='Категория товара или услуги')),
                ('organizations', models.ManyToManyField(through='organizations_directory.Offer', to='organizations_directory.Organization')),
            ],
            options={
                'verbose_name': 'Товар/Услуга',
                'verbose_name_plural': 'Товары/Услуги',
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='offer',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations_directory.organization', verbose_name='Предприятие'),
        ),
        migrations.AddField(
            model_name='offer',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='organizations_directory.product', verbose_name='Продукт/Услуга'),
        ),
    ]
