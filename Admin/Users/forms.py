from core.User.models import User
from core.Utils.Filters.filtersets import BaseFilterForm


class UsersFilterForm(BaseFilterForm):
    class Meta(BaseFilterForm.Meta):
        model = User
        search_fields = ('email',)
        activity_field = 'is_active'
