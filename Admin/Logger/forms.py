import django_filters
from core.Utils.logger import ActivityLog, LevelChoices
from core.Utils.Filters.filtersets import BaseSearchFilterMixin


class LoggerFilterForm(BaseSearchFilterMixin):
    level = django_filters.ChoiceFilter(choices=LevelChoices)

    class Meta(BaseSearchFilterMixin.Meta):
        model = ActivityLog
        fields = ()
        search_fields = ('key', 'description')
