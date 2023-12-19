import django_filters
from django import forms
from django.db.models import Q


class BaseFilterMixin(django_filters.FilterSet):
    class Meta:
        fields = ()


class BaseActiveFilterMixin(BaseFilterMixin):
    is_active = django_filters.ChoiceFilter(label='Is active', empty_label='Not selected', method='is_active_filter',
                                            choices=[('true', 'Active'), ('false', 'Not active')])

    def is_active_filter(self, queryset, name, value):
        if value == 'true':
            queryset = queryset.filter(archived_stamp__isnull=True)
        elif value == 'false':
            queryset = queryset.filter(archived_stamp__isnull=False)
        return queryset

    class Meta(BaseFilterMixin.Meta):
        fields = BaseFilterMixin.Meta.fields + ('is_active',)


class BaseSearchFilterMixin(BaseFilterMixin):
    search = django_filters.CharFilter(label='Search', method='search_qs',
                                       widget=forms.TextInput(attrs={'type': 'search'}))

    def search_qs(self, queryset, name, value):
        fields = self.Meta.search_fields
        _filter = Q()
        for field in fields:
            _filter |= Q(**{f'{field}__icontains': value})
        queryset = queryset.filter(_filter)
        return queryset

    class Meta(BaseFilterMixin.Meta):
        fields = BaseFilterMixin.Meta.fields + ('search',)
        search_fields = ()


class BaseFilterForm(BaseSearchFilterMixin, BaseActiveFilterMixin):
    class Meta(BaseFilterMixin.Meta):
        fields = BaseSearchFilterMixin.Meta.fields + BaseActiveFilterMixin.Meta.fields
        search_fields = ()
