from django import forms

class ExampleForm(forms.Form):
    search_query = forms.CharField(label='Search', max_length=100)