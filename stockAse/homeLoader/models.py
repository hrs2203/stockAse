from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

from .manager import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email_field'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    following = models.ManyToManyField(
        'self', related_name='follows')
    watch_list = models.ManyToManyField(
        'Company', related_name='is_interested_in')
    balance = models.DecimalField(
        max_digits=10, decimal_places=2, default=1000)
    photo = models.ImageField(null=True, blank=True,
                              upload_to="profile_photos/")

    def __str__(self):
        return self.email


class Company(models.Model):
    company_id = models.CharField(
        max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    company_name = models.CharField(max_length=50, blank=False, unique=False)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, blank=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.company_name


class Shares(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    shares_count = models.IntegerField(blank=False)
    shares_sale = models.IntegerField(default=0)


class Transaction(models.Model):
    transaction_id = models.CharField(
        max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    seller = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='Seller')
    buyer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='Buyer')
    status = models.CharField(max_length=50, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    shares_count = models.IntegerField(blank=False)
    time = models.DateTimeField(auto_now_add=True)


class Events(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    event_id = models.CharField(
        max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, blank=False)
    venue = models.CharField(max_length=100, blank=False)
    start_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.DateTimeField(auto_now=False, auto_now_add=False)
    status = models.CharField(max_length=50, blank=False)
