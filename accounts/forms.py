from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_form_style.forms import StyleModelForm
from accounts.models import StdGroupModel, StdReportModel, StdEducationalModel



class UserForm(StyleModelForm):
    group_fields_class = {
        'last_name': 'col-md-4',
        'first_name': 'col-md-4',
    }

    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name']
        
    password = None
    

class StdSearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_form_control = ['first_name', 'last_name']
        for item in list_form_control:
            self.fields[item].widget.attrs['class'] = 'form-control'

    first_name = forms.CharField(max_length=30, required=False)        
    last_name = forms.CharField(max_length=30, required=False)

    
class StdReportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_form_control = ['title', 'desc', 'score']
        for item in list_form_control:
            self.fields[item].widget.attrs['class'] = 'form-control'
            
        self.fields['date'].widget.attrs['class'] = 'form-control datetimepicker'
       
        self.fields['desc'].required = False
        self.fields['score'].required = False
        
    class Meta:
        model = StdReportModel
        exclude = ['student']
        
        
class StdEducationalGoodForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_form_control = ['number', 'score']
        for item in list_form_control:
            self.fields[item].widget.attrs['class'] = 'form-control'
            
        self.fields['good'].widget.attrs['class'] = 'form-select'
        
        self.fields['good'].required = True
        self.fields['number'].required = False
        self.fields['score'].required = False
        
    class Meta:
        model = StdEducationalModel
        exclude = ['student', 'bad']


class StdEducationalbadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_form_control = ['number', 'score']
        for item in list_form_control:
            self.fields[item].widget.attrs['class'] = 'form-control'
            
        self.fields['bad'].widget.attrs['class'] = 'form-select'
        
        self.fields['bad'].required = True
        self.fields['number'].required = False
        self.fields['score'].required = False
        
    class Meta:
        model = StdEducationalModel
        exclude = ['student', 'good']


class StdGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['group'].widget.attrs['class'] = 'form-control'
        self.fields['can_edit'].widget.attrs['class'] = 'form-check-input'
        self.fields['group_name'].widget.attrs['class'] = 'form-select'
        
        self.fields['group'].disabled = True
        self.fields['can_edit'].disabled = True
        self.fields['group_name'].disabled = True

    class Meta:
        model = StdGroupModel
        fields = '__all__' 
        
        
class StdUploadGroupForm(forms.Form):
    file = forms.FileField()
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['file'].widget.attrs['class'] = 'form-control'
        self.fields['file'].widget.attrs['accept'] = ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"
        
        
class ResetPassWord(forms.Form):
    last_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="رمز عبور قبلی")
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="رمز عبور جدید")
    Confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="تایید رمز عبور")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_form_control = ['last_password', 'new_password', 'Confirm_password']
        for item in list_form_control:
            self.fields[item].widget.attrs['class'] = 'form-control'
