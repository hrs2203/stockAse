from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        _('email_field'), unique=True, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    following = models.ManyToManyField(
        'self', related_name='follows')
    watch_list = models.ManyToManyField(
        'Company', related_name='is_interested_in')
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000, verbose_name="Balance Amount")
    photo = models.ImageField(null=True, blank=True,
                              upload_to="profile_photos/", verbose_name="Profile Photo")

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Company(models.Model):
    company_id = models.CharField(
        max_length=50, primary_key=True, unique=True, default=uuid.uuid4, verbose_name="ID")
    company_name = models.CharField(
        max_length=50, blank=False, unique=False, verbose_name="Name")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Owner")
    description = models.CharField(
        max_length=200, blank=True, verbose_name="Description")
    selling_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price")

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class Shares(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    shares_count = models.IntegerField(
        blank=False, verbose_name="Number of shares acquired")
    shares_sale = models.IntegerField(
        default=0, verbose_name="Number of shares on sale")

    class Meta:
        verbose_name = 'Share'
        verbose_name_plural = 'Shares'


class Transaction(models.Model):
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='Seller')
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='Buyer')
    status = models.CharField(max_length=50, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    shares_count = models.IntegerField(
        blank=False, verbose_name="Number of Shares to Purchase", default=0)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'


class Events(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    event_id = models.CharField(
        max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, blank=False)
    venue = models.CharField(max_length=100, blank=False)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
