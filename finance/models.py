from django.db import models

# Create your models here.


class Revenue(models.Model):
    REVENUE_CHOICES = [
        ('rooms', 'Rooms'),
        ('Food & Beverage', 'Food & Beverage'),
        ('party', 'Party'),
        ('other', 'Other')
    ]
    category = models.CharField(max_length=20, choices=REVENUE_CHOICES)
    description = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    received_from = models.CharField(max_length=30, default="staff")
    date = models.DateField()


class Cost_of_sales(models.Model):
    COST = [
        ('retaurant', 'Retaurant'),
        ('accomodation', 'Accomodation'),
        ('party', 'Party'),
        ('other', 'Other')
    ]
    name= models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=COST)
    description = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    drawn = models.CharField(max_length=30, default="staff")
    date = models.DateField()


class Expense(models.Model):
    EXPENCE_CHOICES = [
        ('staff', 'Salaries and Wages'),
        ('utilities', 'Utilities'),
        ('repairs', 'Repairs and Maintenance'),
        ('supplies', 'Cleaning & Room Supplies'),
        ('fnb', 'Food and Beverage'),
        ('admin', 'Administrative'),
        ('marketing', 'Sales and Marketing'),
        ('finance', 'Finance Costs'),
        ('depreciation', 'Depreciation'),
        ('other', 'Other'),

    ]
    category = models.CharField(max_length=30, choices=EXPENCE_CHOICES)
    description = models.TextField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    drawn_by = models.CharField(max_length=30, default="staff")


class Asset(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date_acquired = models.DateField()


class Liability(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
