from django.forms import ModelForm

from mymainapp.models import Brand


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = ['name',]
        labels = {'name': 'Brand'}
        help_texts = {
            'name': 'Enter the name of a brand not yet added to the catalog. After you click submit, you will go back to the candle list page where you can click +Candle and add a candle with the newly created brand.'
        }
