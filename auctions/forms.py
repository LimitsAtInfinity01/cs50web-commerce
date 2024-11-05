from django import forms

class ListingsForm(forms.Form):
    title = forms.CharField()
    description = forms.CharField()
    price = forms.FloatField()
    image_url = forms.URLField(required=False)

    
