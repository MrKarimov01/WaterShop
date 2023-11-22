from collections.abc import Iterable
from django.db import models
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from docx import Document
from django.shortcuts import redirect, render


class Category(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField()
    product_count = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    photo = models.ImageField()
    name = models.CharField(max_length=255)
    LITER_CHOICES = (
        (1, '0.25 liter'),
        (2, '0.5 liter'),
        (3, '1 liter'),
        (4, '1.5 liter'),
        (5, '2 liter'),
        (6, '2.5 liter'),
        (7, '3 liter'),
        (8, '5 liter'),
        (9, '10 liter'),
    )

    liter = models.IntegerField(choices=LITER_CHOICES)
    price = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            # Yangi obyekt yaratilganida product_count ni oshirish
            self.category.product_count += 1
            self.category.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Obyekt o'chirilganda product_count ni kamaytirish
        self.category.product_count -= 1
        self.category.save()
        super().delete(*args, **kwargs)

    def get_display_liter(self):
        return dict(self.LITER_CHOICES)[self.liter]

    def __str__(self):
        return f"{self.name}, {self.get_display_liter()}"


class Output(models.Model):
    price = models.PositiveIntegerField()
    about_the_price = models.TextField()
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)


class Order(models.Model):
    user = models.CharField(max_length=255)
    product1 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="birinchi_mahsulot")
    quantity1 = models.PositiveIntegerField(default=0)
    total1 = models.PositiveIntegerField(default=0)
    product2 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ikkinchi_mahsulot", null=True, blank=True)
    quantity2 = models.PositiveIntegerField(default=0, null=True, blank=True)
    total2 = models.PositiveIntegerField(default=0, null=True, blank=True)
    product3 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="uchinchi_mahsulot", null=True, blank=True)
    quantity3 = models.PositiveIntegerField(default=0, null=True, blank=True)
    total3 = models.PositiveIntegerField(default=0, null=True, blank=True)
    product4 = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tortinchi_mahsulot", null=True, blank=True)
    quantity4 = models.PositiveIntegerField(default=0, null=True, blank=True)
    total4 = models.PositiveIntegerField(default=0, null=True, blank=True)
    total_amount = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.calculate_totals()
        super().save(*args, **kwargs)

    def calculate_totals(self):
        if self.product1:
            self.total1 = self.product1.price * self.quantity1
        else:
            self.total1 = 0

        if self.product2:
            self.total2 = self.product2.price * self.quantity2
        else:
            self.total2 = 0

        if self.product3:
            self.total3 = self.product3.price * self.quantity3
        else:
            self.total3 = 0

        if self.product4:
            self.total4 = self.product4.price * self.quantity4
        else:
            self.total4 = 0
        if not self.pk:
            self.total_amount = self.total1 + self.total2 + self.total3 + self.total4



