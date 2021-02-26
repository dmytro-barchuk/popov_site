import django_filters
from django_filters import CharFilter

from .models import *
from django import forms

class PostFilter(django_filters.FilterSet):

	title = CharFilter(field_name='title', 
		lookup_expr="icontains", 
		label="Введіть назву",
		)
	tags = django_filters.ModelMultipleChoiceFilter(
		queryset=Tag.objects.all(), 
		widget=forms.CheckboxSelectMultiple,
		label="Оберіть категорії",
		)

	class Meta:
		model = Post
		fields = ['title', 'tags']


