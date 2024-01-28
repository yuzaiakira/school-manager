from django import forms
from django.contrib.auth.forms import UserChangeForm
from django_form_style.forms import StyleModelForm
from information import models


class StdInfoForm(StyleModelForm):
    fields_class = {
        'birthday': 'date-picker'
    }
    group_fields_class = {
        'id_code': 'col-md-4',

        'certificate_place': 'col-md-4',
        'certificate_Zone': 'col-md-4',
        'serial': 'col-md-4',

        'serial_char': 'col-md-3',
        'serial_number': 'col-md-3',
        'birth_place': 'col-md-3',
        'birthday': 'col-md-3',

        'physical_condition': 'col-md-6',
        'hands': 'col-md-6',

        'family_size': 'col-md-3',
        'child_num': 'col-md-3',
        'bro_num': 'col-md-3',
        'sis_num': 'col-md-3',

        'place': 'col-md-4',
        'live_with': 'col-md-4',
        'insurance': 'col-md-4',

        'veteran_percentage': 'col-md-6',
        'sacrifice_code': 'col-md-6',

        'legal_guardian': 'col-md-6',
        'legal_guardian_id': 'col-md-6',

    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        fields_name = ['family_size', 'child_num', 'bro_num', 'sis_num']
        for field in fields_name:
            self.fields[field].widget.attrs['min'] = 0
            self.fields[field].widget.attrs['max'] = 20

        self.fields['veteran_percentage'].widget.attrs['min'] = 0
        self.fields['veteran_percentage'].widget.attrs['max'] = 100

    class Meta:
        model = models.StdInfoModel
        exclude = ['user', 'pic']


class UserForm(StyleModelForm):
    group_fields_class = {
        'last_name': 'col-md-4',
        'first_name': 'col-md-4',
    }

    class Meta(UserChangeForm.Meta):
        fields = ['first_name', 'last_name']

    password = None


class FatherInfoForm(StyleModelForm):
    group_fields_class = {
        'last_name': 'col-md-4',
        'first_name': 'col-md-4',
        'certificate_num': 'col-md-4',

        'birthday': 'col-md-4',
        'id_code': 'col-md-4',
        'certificate_place': 'col-md-4',

        'is_dead': 'col-md-4',
        'marital': 'col-md-4',
        'education': 'col-md-4',

        'work': 'col-md-6',
        'work_name': 'col-md-6',
    }
    fields_class = {
        'cooperation': 'form-group',
        'birthday': 'date-picker'
    }

    class Meta:
        model = models.FatherInfoModel
        exclude = ['student']


class MotherInfoForm(FatherInfoForm):
    group_fields_class = {
        'last_name': 'col-md-4',
        'first_name': 'col-md-4',
        'certificate_num': 'col-md-4',

        'birthday': 'col-md-4',
        'id_code': 'col-md-4',
        'is_dead': 'col-md-4',

        'marital': 'col-md-6',
        'education': 'col-md-6',

        'work': 'col-md-6',
        'work_name': 'col-md-6',
    }

    class Meta:
        model = models.MatherInfoModel
        exclude = ['student']


class SupervisorInfoForm(FatherInfoForm):
    group_fields_class = {
        'last_name': 'col-md-4',
        'first_name': 'col-md-4',
        'certificate_num': 'col-md-4',

        'birthday': 'col-md-4',
        'id_code': 'col-md-4',
        'certificate_place': 'col-md-4',

        'relationship': 'col-md-6',
        'marital': 'col-md-6',

        'is_dead': 'col-md-6',
        'education': 'col-md-6',

        'work': 'col-md-6',
        'work_name': 'col-md-12',
    }

    class Meta:
        model = models.SupervisorInfoModel
        exclude = ['student']


class StdLastSchoolForm(StyleModelForm):
    group_fields_class = {
        'last_school': 'col-md-6',
        'last_city': 'col-md-6',

        'phone': 'col-md-6',
        'score': 'col-md-6',
    }

    class Meta:
        model = models.StdLastSchoolModel
        exclude = ['student']


class StdCompetitionsForm(StyleModelForm):
    group_fields_class = {
        'sport': 'col-md-6',
        'sport_rank': 'col-md-6',
    }
    fields_class = {
        'quranic': 'form-group',
        'academic': 'form-group',
        'cultural': 'form-group',
        'cooperation': 'form-group',
    }

    class Meta:
        model = models.StdCompetitionsModel
        exclude = ['student']


class StdShadForm(StyleModelForm):
    group_fields_class = {
        'smartphone': 'col-md-6',
        'shad_phone': 'col-md-6',
    }

    class Meta:
        model = models.StdShadModel
        exclude = ['student']


class StdPlaceInfoForm(StyleModelForm):
    group_fields_class = {
        'main_St': 'col-md-6',
        'auxiliary_St': 'col-md-6',

        'main_street': 'col-md-6',
        'side_alley': 'col-md-6',

        'plaque': 'col-md-4',
        'floor': 'col-md-4',
        'postal_code': 'col-md-4',

        'home_phone': 'col-md-3',
        'dad_phone': 'col-md-3',
        'mom_phone': 'col-md-3',
        'std_phone': 'col-md-3',

        'dad_workplace_phone': 'col-md-6',
        'mom_workplace_phone': 'col-md-6',

        'supervisor_phone': 'col-md-6',
        'sms_phone': 'col-md-6',

    }

    class Meta:
        model = models.StdPlaceInfoModel
        exclude = ['student']



