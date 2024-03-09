from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView


from accounts.forms import (StdSearchForm, StdReportForm, StdGroupForm,
                            StdUploadGroupForm, ResetPassWord, UserForm)
from accounts.models import UserModel, StdGroupModel, StdReportModel, StdEducationalModel
from accounts.functions import import_csv_file
from accounts.mixin import UserAuthorizationMixin

from information.models import (StdInfoModel, FatherInfoModel, MatherInfoModel, SupervisorInfoModel, StdLastSchoolModel,
                                StdCompetitionsModel, StdShadModel, StdPlaceInfoModel)
import information.forms as info_form
from payments.models import UserPriceModel
from payments.functions import price_peer_part
from blog.models import PostModel

from core.settings import REDIRECT_FIELD_NAME

from jalali_date import datetime2jalali


# Create your views here.
@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def account_view(request):
    # change is in to ==
    if request.user.first_name == '' and request.user.last_name == '':
        name = "به سایت خوش آمدید."
    else:
        name = request.user.first_name + " " + request.user.last_name
        
    post = PostModel.objects.all().order_by('-id')
    paginator = Paginator(post, 10)    
    result = paginator.page(1)
    
    context = {
        'info': {
                 'name': name,
                 'last_login': datetime2jalali(request.user.last_login).strftime('%Y/%m/%d - %H:%M:%S'),
                 'date_joined': datetime2jalali(request.user.date_joined).strftime('%Y/%m/%d - %H:%M:%S'),
                 },
        'blog': result
    
    }
    if request.user.is_staff:
      pass

    return render(request, "accounts/home.html", context)


class HomeAccount(View):
    template_name = "accounts/home.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_staff:
            return self.admin(request)

        return self.client(request)

    def client(self, request):
        context = self.get_context_data()
        context['reports'] = StdReportModel.objects.filter(student__id=request.user.StdInfoModel.id)
        context['educational'] = StdEducationalModel.get_data(request.user.StdInfoModel.id)

        return render(request, self.template_name, context)

    def admin(self, request):
        return render(request, self.template_name)

    def get_context_data(self):
        return dict()


class Login(LoginView):
    redirect_authenticated_user = True
    template_name = "accounts/login.html"
    redirect_field_name = settings.REDIRECT_FIELD_NAME

    def get_success_url(self):
        return settings.LOGIN_REDIRECT_URL

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class StdList(UserAuthorizationMixin, ListView):
    permission_required = 'UserModel.user_serach'

    model = StdInfoModel
    template_name = "accounts/student-list.html"
    paginate_by = 50

    form = StdSearchForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form(initial=self.get_search_value())
        context['current_url'] = self.get_current_url()
        return context

    def get_queryset(self):
        data = self.get_search_value()
        queryset = super().get_queryset()
        filter_val = dict()

        if data['id_code']:
            filter_val.update({'id_code__icontains': data['id_code']})
        if data['first_name']:
            filter_val.update({'user__first_name__icontains': data['first_name']})
        if data['last_name']:
            filter_val.update({'user__last_name__icontains': data['last_name']})
        if data['class_name']:
            filter_val.update({'user__group__group_name__icontains': data['class_name']})

        return queryset.filter(**filter_val).only('id_code',
                                                  'user__first_name',
                                                  'user__last_name',
                                                  'user__group__group_name')

    def get_search_value(self) -> dict:
        search_fields = dict()
        search_fields['first_name'] = self.request.GET.get('first_name')
        search_fields['last_name'] = self.request.GET.get('last_name')
        search_fields['id_code'] = self.request.GET.get('id_code')
        search_fields['class_name'] = self.request.GET.get('class_name')
        search_fields['page'] = self.request.GET.get('page')

        return search_fields
    def get_current_url(self):
        url = "?"
        search_fields = self.get_search_value()
        for key in search_fields:
            value = search_fields[key]
            if value and key != "page":
                url += f"&{key}={value}"
            else:
                url += f"&{key}="

        return url


class ManageStudents(UserAuthorizationMixin, TemplateView):
    permission_required = 'StdInfoModel.view_stdinfomodel'
    template_name = "accounts/manage-student.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']

        context["student"] = get_object_or_404(StdInfoModel, pk=student_id)
        context["reports"] = StdReportModel.objects.filter(student=context["student"])
        context["educational"] = StdEducationalModel.get_data(student_id)
        context["payments"] = UserPriceModel.objects.filter(user__pk=context["student"].user.pk)

        # TODO: make pyment
        for total_price in context['payments']:
            if not price_peer_part(total_price):
                total_price.finished = True
                total_price.save

        return context


class StudentInfo(UserAuthorizationMixin, TemplateView):
    permission_required = 'StdInfoModel.view_stdinfomodel'
    template_name = "accounts/manage-student-info.html"
    models =[StdInfoModel, FatherInfoModel, MatherInfoModel, SupervisorInfoModel, StdLastSchoolModel,
             StdCompetitionsModel, StdShadModel, StdPlaceInfoModel]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['student_id']

        context['student'] = get_object_or_404(StdInfoModel, pk=student_id)
        context['forms'] = self.get_forms(context['student'])

        return context

    def get_forms(self, student) -> list:
        forms = list()

        father, father_status = FatherInfoModel.objects.get_or_create(student=student)
        mather, mather_status = MatherInfoModel.objects.get_or_create(student=student)
        supervisor, supervisor_status = SupervisorInfoModel.objects.get_or_create(student=student)
        lastschool, lastschool_status = StdLastSchoolModel.objects.get_or_create(student=student)
        competitions, competitions_status =StdCompetitionsModel.objects.get_or_create(student=student)
        shad, shad_status = StdShadModel.objects.get_or_create(student=student)
        place, place_status = StdPlaceInfoModel.objects.get_or_create(student=student)

        # append forms to list
        forms.append(UserForm(instance=student.user))
        forms.append(info_form.StdInfoForm(instance=student))
        forms.append(info_form.FatherInfoForm(instance=father))
        forms.append(info_form.MotherInfoForm(instance=mather))
        forms.append(info_form.SupervisorInfoForm(instance=supervisor))
        forms.append(info_form.StdLastSchoolForm(instance=lastschool))
        forms.append(info_form.StdCompetitionsForm(instance=competitions))
        forms.append(info_form.StdShadForm(instance=shad))
        forms.append(info_form.StdPlaceInfoForm(instance=place))

        return forms


@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def group_view(request):
    if request.user.is_staff:
        group = StdGroupModel.objects.all()

        context={
            'groups': group
        }
        return render(request, "accounts/manage-student-group.html", context)
    
    else:
        raise Http404



@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def group_upload_view(request, group_id):
    if request.user.is_staff:
        get_group = get_object_or_404(StdGroupModel, pk=group_id)
        form  = StdGroupForm(instance=get_group)
        
        if request.method == 'POST':  
            fileform = StdUploadGroupForm(request.POST, request.FILES)  
            if fileform.is_valid():  
                import_csv_file(request.FILES['file'], get_group, UserModel)  
                
                return render(request, "accounts/page-upload-successful.html")
        else:  
            fileform = StdUploadGroupForm()  
            
            context={
                'group': form,
                'formfile': fileform,
                
            }
            return render(request, "accounts/manage-student-group-upload.html", context)
    
    else:
        raise Http404



@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def reset_password_view(request):
    context={}
    if request.method == "POST":
        rp_form = ResetPassWord(request.POST)
        user = request.user
        if rp_form.is_valid():
            last_password =  rp_form.cleaned_data['last_password']
            new_password =   rp_form.cleaned_data['new_password']
            Confirm_password =   rp_form.cleaned_data['Confirm_password']
        
            authenticate_user = authenticate(request, username=user.username, password=last_password)
        
            if (authenticate_user is not None) and \
                (new_password == Confirm_password) and \
                (new_password != last_password):
                    
                try:
                    user.set_password(new_password)
                    user.save()
                    context['notice'] = "رمز عبور با موفقیت تغییر کرد"
                except:
                    context['erro_text'] = "یک اشتباهی رخ داده است"
                    
               
                
            else:
                context['erro_text'] = "اطلاعات وارد شده غلط میباشد"
            
        else:
            context['erro_text'] = "یک اشتباهی رخ داده است"
            
        
    
    else:
        rp_form = ResetPassWord()
        
        
    context['form'] = rp_form
    return render(request,'accounts/profile-reset-password.html', context)


def error_404_view(request, exception):
    return render(request, 'accounts/page-404.html')


def error_403_view(request, exception):
    return render(request, 'base/page-403.html')
