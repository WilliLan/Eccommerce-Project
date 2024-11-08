from django import forms

class PaymentForm(forms.Form):
    full_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Name on Card'}), max_length=100, required=True)
    address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 1'}), max_length=100, required=True)
    address2 = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Address 2'}), max_length=100, required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing City'}), required=True, max_length=50)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing State - 2 Digits'}), required=True, max_length=2)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Billing Zipcode'}), max_length=10, required=True)
    card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Card Number'}), max_length=16, required=True)
    exp_month = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Exp Month (2 Digits)'}), required=True, max_length=2)
    exp_year = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Exp Year (4 Digits)'}), max_length=4, required=True)
    cvv = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'CVV Code'}), max_length=3, required=True)




'''
class PaymentForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    address1 = forms.CharField(max_length=100)
    address2 = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=50)
    state = forms.CharField(max_length=2)
    zipcode = forms.CharField(max_length=10)
    phone = forms.CharField(max_length=20)
    card_number = forms.CharField(max_length=16)
    exp_month = forms.CharField(max_length=2)
    exp_year = forms.CharField(max_length=4)
    cvv = forms.CharField(max_length=3)
'''