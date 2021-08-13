from django import forms
from menu.models import Menu,Category

class MenuForm(forms.ModelForm):
	class Meta:
		model = Menu
		fields = '__all__'
		exclude = ("slug",)
		category = forms.MultipleChoiceField()
		widgets = {
			'category': forms.CheckboxSelectMultiple(attrs={'id':'multicb','class':'form-control','multiple': True,'type':'checkbox'}),
			'name': forms.TextInput(attrs={'placeholder':'Menu Name','class':'form-control mb-3'}),
			'size': forms.Select(attrs={'placeholder':'size','class':'form-control mb-3'}),
			'price': forms.NumberInput(attrs={'placeholder':'price','class':'form-control mb-3'}),
			'image': forms.ClearableFileInput(attrs={'class':'form-control','accept':"image/*"}),
		}

class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = '__all__'
		exclude = ("slug",)
		widgets = {
			'name': forms.TextInput(attrs={'placeholder':'Category Name','class':'form-control mb-3'}),
			'image': forms.ClearableFileInput(attrs={'class':'form-control','accept':"image/*"}),
		}