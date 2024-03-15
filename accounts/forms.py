import os
import pandas as pd

from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.hashers import make_password
from django_form_style.forms import StyleModelForm, StyleForm

from accounts.models import UserModel

class UserForm(StyleModelForm):
    group_fields_class = {
        'last_name': 'col-md-4',
        'first_name': 'col-md-4',
    }

    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name']
        
    password = None
    

class StdSearchForm(StyleForm):
    first_name = forms.CharField(max_length=255, label="نام", required=False)
    last_name = forms.CharField(max_length=255, label="نام خانوادگی", required=False)
    id_code = forms.CharField(max_length=20, label="کدملی", required=False)
    class_name = forms.CharField(max_length=255, label="کلاس", required=False)


class StdUploadGroupForm(forms.Form):
    file = forms.FileField(label="فایل مشخصات")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['file'].widget.attrs['accept'] = ".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"

    def import_from_file(self, group_obj):
        base_file = self.make_file()
        dataframe = pd.read_excel(base_file)

        for row in dataframe.index:
            user, created = UserModel.objects.update_or_create(
                            username=str(dataframe.iloc[row, 0]),
                            defaults={'password': make_password(str(dataframe.iloc[row, 1])),
                                      'group': group_obj}
                        )

        # remove file
        os.remove(base_file)

    def make_file(self) -> bytes:
        """
        make file in safe dir wen uploaded
        :return: file address
        """
        file = self.cleaned_data["file"]
        base_file = os.path.join(settings.BASE_DIR, 'safedir/csv/') + file.name
        # create file
        with open(base_file, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        return base_file


class ResetPassWord(forms.Form):
    last_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="رمز عبور قبلی")
    new_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="رمز عبور جدید")
    Confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput(), label="تایید رمز عبور")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        list_form_control = ['last_password', 'new_password', 'Confirm_password']
        for item in list_form_control:
            self.fields[item].widget.attrs['class'] = 'form-control'
