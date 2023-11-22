# Generated by Django 4.2.6 on 2023-11-10 16:48

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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('photo', models.ImageField(upload_to='')),
                ('product_count', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Output',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.PositiveIntegerField()),
                ('about_the_price', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to='')),
                ('name', models.CharField(max_length=255)),
                ('liter', models.IntegerField(choices=[(1, '0.25 liter'), (2, '0.5 liter'), (3, '1 liter'), (4, '1.5 liter'), (5, '2 liter'), (6, '2.5 liter'), (7, '3 liter'), (8, '5 liter'), (9, '10 liter')])),
                ('price', models.PositiveIntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=255)),
                ('quantity1', models.PositiveIntegerField(default=0)),
                ('total1', models.PositiveIntegerField(default=0)),
                ('quantity2', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total2', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('quantity3', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total3', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('quantity4', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total4', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('total_amount', models.PositiveIntegerField(default=0)),
                ('date', models.DateField(auto_now_add=True)),
                ('time', models.TimeField(auto_now_add=True)),
                ('product1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='birinchi_mahsulot', to='main.product')),
                ('product2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ikkinchi_mahsulot', to='main.product')),
                ('product3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='uchinchi_mahsulot', to='main.product')),
                ('product4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tortinchi_mahsulot', to='main.product')),
            ],
        ),
    ]