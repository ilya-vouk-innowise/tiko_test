from django_filters import BooleanFilter, FilterSet

from events.models import Event


class EventFilter(FilterSet):
    my_only = BooleanFilter(method="filter_by_my_only")

    def filter_by_my_only(self, queryset, value: bool, *args, **kwargs):
        if value and self.request.user and self.request.user.is_authenticated:
            queryset = queryset.filter(creator=self.request.user)
        return queryset

    class Meta:
        model = Event
        fields = {
            "name": ["exact", "icontains", "istartswith"],
            "start_date": ["gte", "lte"],
            "end_date": ["gte", "lte"],
            "creator": ["exact"],
        }
