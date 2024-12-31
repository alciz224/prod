import django_filters
from django.db.models import Q
from datetime import date, timedelta

# Utility functions for calculating date ranges
def get_week_range(today):
    start_of_week = today - timedelta(days=today.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def get_month_range(today):
    start_of_month = today.replace(day=1)
    next_month = today.replace(day=28) + timedelta(days=4)
    start_of_next_month = next_month.replace(day=1)
    end_of_month = start_of_next_month - timedelta(days=1)
    return start_of_month, end_of_month

def get_year_range(today):
    start_of_year = today.replace(month=1, day=1)
    end_of_year = today.replace(month=12, day=31)
    return start_of_year, end_of_year

# Generic Date Range Filter class
class MyBaseFilter(django_filters.FilterSet):
    filter_by = django_filters.ChoiceFilter(
        choices=[('week', 'This Week'), ('month', 'This Month'), ('year', 'This Year')],
        method='filter_by_range',
        label='Filter by Date Range'
    )


    def get_date_field(self):
        """
        Return the appropriate date field for filtering.
        Override this method in each filter class if different models
        use different date fields.
        """
        raise NotImplementedError

    def filter_by_range(self, queryset, name, value):
        today = date.today()

        # Define the date range based on filter choice
        if value == 'week':
            start_date, end_date = get_week_range(today)
        elif value == 'month':
            start_date, end_date = get_month_range(today)
        elif value == 'year':
            start_date, end_date = get_year_range(today)
        else:
            return queryset

        # Dynamically filter based on the date field
        date_field = self.get_date_field()
        return queryset.filter(
            Q(**{f"{date_field}__gte": start_date}) & Q(**{f"{date_field}__lte": end_date})
        )


from .models import Post

class PostFilter(MyBaseFilter):
    def get_date_field(self):
        # Return the date field name for the Post model
        return 'created_at'

    class Meta:
        model = Post
        fields = ['filter_by']

from .models import Event

class EventFilter(MyBaseFilter):

    category = django_filters.CharFilter(
        field_name="category",
        lookup_expr="icontains",
        label="Catégorie"
    )
    def get_date_field(self):
        # Return the date field name for the Event model
        return 'start_date'

    class Meta:
        model = Event
        fields = ['filter_by', 'category']
