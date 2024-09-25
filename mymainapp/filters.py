import django_filters

from mymainapp.models import Candle, Brand, ScentGenre


class CandleFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    genre_2 = django_filters.ModelChoiceFilter(field_name='notes__genre', queryset=ScentGenre.objects.all())
    class Meta:
        model = Candle
        fields = ['brand_id', 'notes__genre',]

    def __init__(self, *args, **kwargs):
        super(CandleFilter, self).__init__(*args, **kwargs)
        self.filters['brand_id'].label="Brand"
        self.filters['notes__genre'].label = "Note genre"
