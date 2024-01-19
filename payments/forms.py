from django import forms

from payments.models import UserPaymentModel, UserPriceModel


class UserPaymentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['date'].widget.attrs['class'] = 'form-control datetimepicker'
        self.fields['price'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = UserPaymentModel
        fields = ['date', 'price', 'description']


class UserPriceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['total_price'].widget.attrs['class'] = 'form-select'
        self.fields['Installment'].widget.attrs['class'] = 'form-check'
        self.fields['finished'].widget.attrs['class'] = 'form-check'

    class Meta:
        model = UserPriceModel
        fields = ['total_price', 'Installment', 'finished']
