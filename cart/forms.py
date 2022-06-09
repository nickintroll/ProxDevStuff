from django import forms

PRODUCT_UQAUNTITY_CHOICE = [(i, str(i)) for i in range(1,19)]

class CartAddProductForm(forms.Form):
	quantity =  forms.TypedChoiceField(
		choices = PRODUCT_UQAUNTITY_CHOICE,
		coerce=int
	)
	override = forms.BooleanField(
		required=False,
		initial=False,
		widget=forms.HiddenInput
	)

