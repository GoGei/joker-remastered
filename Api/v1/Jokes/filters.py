from django_filters import rest_framework


class AccountJokesFilter(rest_framework.FilterSet):
    is_liked = rest_framework.BooleanFilter(field_name='is_liked_by_user_annotated', method='filter_is_liked')

    def filter_is_liked(self, queryset, name, value):
        if value is not None:
            return queryset.filter(is_liked_by_user_annotated=value)
        return queryset
