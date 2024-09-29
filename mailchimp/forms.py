from django import forms


class MailchimpSubscribeForm(forms.Form):
    email = forms.EmailField(label="Enter your email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email Address'
    }))
