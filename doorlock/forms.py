from django import forms


class DoorlockCreationForm(forms.Form):
    beacon_id = forms.IntegerField()
    push_id = forms.IntegerField()