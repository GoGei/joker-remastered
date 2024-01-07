import django_mongoengine_filter
from mongoengine import Q
from django.utils.translation import gettext_lazy as _
from core.Utils.logger import ActivityLog, LevelChoices
from core.Utils.Filters.filtersets import BaseSearchFilterMixin

empty_value = '', _('Select')
choices = (empty_value,) + tuple(LevelChoices.choices)


class LoggerFilterForm(django_mongoengine_filter.FilterSet):
    level = django_mongoengine_filter.ChoiceFilter(choices=choices,
                                                   required=False)
    search = django_mongoengine_filter.MethodFilter(action='search_filter')

    class Meta(BaseSearchFilterMixin.Meta):
        model = ActivityLog
        fields = ('search', 'level')
        search_fields = ('key', 'description', 'user_id', 'obj_id')

    def search_filter(self, queryset, name, value):
        fields = self.Meta.search_fields
        _filter = Q()
        for field in fields:
            _filter |= Q(**{f'{field}__icontains': value})
        queryset = queryset.filter(_filter)
        return queryset
