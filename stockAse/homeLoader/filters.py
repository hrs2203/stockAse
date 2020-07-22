from .models import Shares
import django_filters


class SharesFilter(django_filters.FilterSet):

    shares_sale = django_filters.NumberFilter(lookup_expr='gt')
    company__company_name = django_filters.CharFilter(lookup_expr='icontains')
    company__selling_price__gt = django_filters.NumberFilter(
        field_name='company__selling_price', lookup_expr='gt')
    company__selling_price__lt = django_filters.NumberFilter(
        field_name='company__selling_price', lookup_expr='lt')

    class Meta:
        model = Shares
        exclude = ['company', 'user', 'shares_count']
