import django_filters
from accounts.models import Professional
from django_filters.widgets import BooleanWidget, RangeWidget
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserFilter(django_filters.FilterSet):
    phone = django_filters.CharFilter()
    email = django_filters.CharFilter()
    username = django_filters.CharFilter()
    professional = django_filters.ChoiceFilter(
        field_name="professional__level", choices=Professional.LEVEL_CHOICES
    )
    is_active = django_filters.BooleanFilter(widget=BooleanWidget())
    is_superuser = django_filters.BooleanFilter(widget=BooleanWidget())

    created_at = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"placeholder": "YYYY/MM/DD"})
    )

    class Meta:
        model = User
        fields = [
            "phone",
            "email",
            "username",
            "professional",
            "is_active",
            "is_superuser",
            "created_at",
        ]
