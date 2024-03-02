from django_filters.rest_framework import FilterSet
import django_filters

from users.models import CustomUser


class StudentFilter(FilterSet):
    group__name = django_filters.CharFilter(field_name='group__name', lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = {
            "first_name": ["icontains"],
            "last_name": ["icontains"],
            "group__name": ["icontains"],  # Use group__name to reference the related group's name field
        }

