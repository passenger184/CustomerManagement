import django_filters
from django_filters import DateFilter,CharFilter

from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created', lookup_expr='gte') #look up expresion greater than or equal to (gte)
    end_date = DateFilter(field_name='date_created', lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains') #icontains means case insensitive
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']