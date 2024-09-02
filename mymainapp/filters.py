import django_filters

from mymainapp.models import Candle, Brand


class CandleFilter(django_filters.FilterSet):

    class Meta:
        model = Candle
        fields = ['brand_id', 'notes__genre']

    def __init__(self, *args, **kwargs):
        super(CandleFilter, self).__init__(*args, **kwargs)
        self.filters['brand_id'].label="Brand"
        self.filters['notes__genre'].label = "Note genre"
