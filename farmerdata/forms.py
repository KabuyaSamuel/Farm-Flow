from django import forms
from farmflow.models import ValueChainChoice, Crop, Farm
from django.core.exceptions import ValidationError

class ValueChainForm(forms.ModelForm):
    class Meta:
        model = ValueChainChoice
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if ValueChainChoice.objects.filter(name=name).exists():
            raise forms.ValidationError("This value chain choice already exists.")
        return name

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'description', 'value_chain']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Crop.objects.filter(name=name).exists():
            raise forms.ValidationError('A crop with this name already exists.')
        return name

class FarmForm(forms.ModelForm):
    class Meta:
        model = Farm
        fields = ['location', 'crops', 'length', 'width','soil_test', 'water_source', 'farming_type', 'value_chains']

