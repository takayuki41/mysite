from django import forms
from . import models

class SearchForm(forms.Form):
    q = forms.CharField(label="検索")