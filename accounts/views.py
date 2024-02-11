from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.conf import settings
from django.core.paginator import Paginator
from django.views import View
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView


from accounts.forms import (StdSearchForm, StdReportForm, StdEducationalGoodForm, StdEducationalbadForm, StdGroupForm,
                            StdUploadGroupForm, ResetPassWord)
from accounts.models import UserModel, StdGroupModel, StdReportModel, StdEducationalModel
from accounts.functions import import_csv_file

from information.models import (StdInfoModel, FatherInfoModel, MatherInfoModel, SupervisorInfoModel, StdLastSchoolModel,
                                StdCompetitionsModel, StdShadModel, StdPlaceInfoModel)

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


class StdList(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.REDIRECT_FIELD_NAME
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

        return queryset.filter(**filter_val).only('id_code', 'user__first_name', 'user__last_name', 'user__group__group_name')

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

@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def manage_student_view(request, student_id):
    if request.user.is_staff:
        student = get_object_or_404(StdInfoModel, pk=student_id)

        context = {
            'student': student,
            'reports': StdReportModel.objects.filter(student=student),
            'educational': {
                'good': StdEducationalModel.objects.filter(student=student, bad=None),
                'bad': StdEducationalModel.objects.filter(student=student, good=None),
            },
            'payments' : UserPriceModel.objects.filter(user__pk=student.user.pk)

        }
        for total_price in context['payments']:
            if not price_peer_part(total_price):
                total_price.finished = True
                total_price.save

        return render(request, "accounts/manage-student.html", context)
    
    else:
        raise Http404
    
    


@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def student_info_view(request, student_id):
    if request.user.is_staff:
        #TODO: fix bug
        student = get_object_or_404(StdInfoModel, pk=student_id)
        father = get_object_or_404(FatherInfoModel, child=student)
        mather = get_object_or_404(MatherInfoModel, child=student)
        supervisor = get_object_or_404(SupervisorInfoModel, child=student)
        lastschool = get_object_or_404(StdLastSchoolModel, student=student)
        competitions = get_object_or_404(StdCompetitionsModel, student=student)
        shad = get_object_or_404(StdShadModel, student=student)
        place = get_object_or_404(StdPlaceInfoModel, student=student)
        
        # StdInfo_Form = StdInfoForm(instance=student)
        # User_Form = UserForm(instance=student.student)
        # FatherInfo_Form = FatherInfoForm(instance=father)
        # MotherInfo_Form = MotherInfoForm(instance=mather)
        # SupervisorInfo_Form = SupervisorInfoForm(instance=supervisor)
        # StdLastSchool_Form = StdLastSchoolForm(instance=lastschool)
        # StdCompetitions_Form = StdCompetitionsForm(instance=competitions)
        # StdShad_Form = StdShadForm(instance=shad)
        # StdPlaceInfo_Form = StdPlaceInfoForm(instance=place)
        
        context={
            # 'StdInfo': StdInfo_Form,
            # 'uinfo': User_Form,
            # 'FatherInfo': FatherInfo_Form,
            # 'MotherInfo': MotherInfo_Form,
            # 'SupervisorInfo': SupervisorInfo_Form,
            # 'LastSchool': StdLastSchool_Form,
            # 'Competitions': StdCompetitions_Form,
            # 'Shad': StdShad_Form,
            # 'PlaceInfo': StdPlaceInfo_Form,
        } 
        
        return render(request, "accounts/manage-student-info.html", context)
    
    else:
        raise Http404


@login_required(None,REDIRECT_FIELD_NAME) 
def report_create_view(request, student_id):
    if request.user.is_staff:
        has_error = False
        student = get_object_or_404(StdInfoModel, pk=student_id)
        StdReport_Form = StdReportForm()
        
        if request.method=="POST":
            if StdReport_Form.is_valid:
                Report = StdReportModel.objects.create(student=student)
                StdReport_Form = StdReportForm(request.POST, instance=Report)
                try:
                    StdReport_Form.save()
                except ValueError:
                    has_error = True
            
            return HttpResponseRedirect(reverse_lazy('manage-student', kwargs={'student_id': student_id}))    
        

        context={
            'report': StdReport_Form,
            'student_id': student_id,
            'text': "افزودن",
            'has_error': has_error
        }    
        return render(request, "accounts/manage-student-add-report.html", context)
    
    else:
        raise Http404



class ReportDelete(DeleteView):
    model = StdReportModel
    context_object_name = 'report'

 
    def form_valid(self, form):
        messages.success(self.request, "The report was deleted successfully.")
        return super(ReportDelete, self).form_valid(form)

    def get_success_url(self):
        object = self.get_object()
        std_id = object.student.pk
        return reverse_lazy('manage-student', kwargs={'student_id': std_id})
 
 
    
@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def report_update_view(request, report_id):
    if request.user.is_staff:
        has_error = False
        report = get_object_or_404(StdReportModel, pk=report_id)
        StdReport_Form = StdReportForm(instance=report)
        
        if request.method == "POST":
            if StdReport_Form.is_valid:

                StdReport_Form = StdReportForm(request.POST, instance=report)
                try:
                    StdReport_Form.save()
                except ValueError:
                    has_error = True
            
            return HttpResponseRedirect(reverse_lazy('manage-student', kwargs={'student_id': report.student.pk}))    
        

        context={
            'report': StdReport_Form,
            'student_id': report.student.pk,
            'text': "ویرایش",
            'has_error': has_error
        }    
        return render(request, "accounts/manage-student-add-report.html", context)
    
    else:
        raise Http404





@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def Educational_good_create_view(request, student_id):
    if request.user.is_staff:
        has_error = False
        student = get_object_or_404(StdInfoModel, pk=student_id)
        StdEducational_Form = StdEducationalGoodForm()
        
        if request.method == "POST":
           
            if StdEducational_Form.is_valid:
                
                educational = StdEducationalModel.objects.create(student=student)
                StdEducational_Form = StdEducationalGoodForm(request.POST, instance=educational)
                try:
                    StdEducational_Form.save()
                except ValueError:
                    has_error= True
            
            return HttpResponseRedirect(reverse_lazy('manage-student', kwargs={'student_id': student_id}))    
        

        context={
            'educational': StdEducational_Form,
            'student_id': student_id,
            'type': "افزودن",
            'text': "مثبت",
            'has_error': has_error
        }    
        return render(request, "accounts/manage-student-educational.html", context)
    
    else:
        raise Http404
    
    

class EducationalDelete(DeleteView):
    model = StdEducationalModel
    context_object_name = 'educational'

 
    def form_valid(self, form):
        messages.success(self.request, "The report was deleted successfully.")
        return super(EducationalDelete, self).form_valid(form)

    def get_success_url(self):
        object = self.get_object()
        std_id = object.student.pk
        return reverse_lazy('manage-student', kwargs={'student_id': std_id})
 
 
@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def Educational_good_update_view(request, edu_id):
    if request.user.is_staff:
        has_error = False
        edu = get_object_or_404(StdEducationalModel, pk=edu_id)
        
        StdEducational_Form = StdEducationalGoodForm(instance=edu)
        
        if request.method == "POST":
            if StdEducational_Form.is_valid:

                StdEducational_Form = StdEducationalGoodForm(request.POST, instance=edu)
                try:
                    StdEducational_Form.save()
                except ValueError:
                    has_error = True
            
            return HttpResponseRedirect(reverse_lazy('manage-student', kwargs={'student_id': edu.student.pk}))    
        

        context={
            'educational': StdEducational_Form,
            'student_id': edu.student.pk,
            'type': "ویرایش",
            'text': "مثبت",
            'has_error': has_error
        }    
        return render(request, "accounts/manage-student-educational.html", context)
    
    else:
        raise Http404




@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def Educational_bad_create_view(request, student_id):
    if request.user.is_staff:
        has_error = False
        student = get_object_or_404(StdInfoModel, pk=student_id)
        StdEducational_Form = StdEducationalbadForm()
        
        if request.method=="POST":
            if StdEducational_Form.is_valid:
                educational = StdEducationalModel.objects.create(student=student)
                StdEducational_Form = StdEducationalbadForm(request.POST, instance=educational)
                try:
                    StdEducational_Form.save()
                except ValueError:
                    has_error = True
            
            return HttpResponseRedirect(reverse_lazy('manage-student', kwargs={'student_id': student_id}))    
        

        context={
            'educational': StdEducational_Form,
            'student_id': student_id,
            'type': "افزودن",
            'text': "منفی",
            'has_error': has_error
        }    
        return render(request, "accounts/manage-student-educational.html", context)
    
    else:
        raise Http404
    


@login_required(redirect_field_name=REDIRECT_FIELD_NAME) 
def Educational_bad_update_view(request, edu_id):
    if request.user.is_staff:
        has_error= False
        edu = get_object_or_404(StdEducationalModel, pk=edu_id)
        StdEducational_Form = StdEducationalGoodForm(instance=edu)
        
        if request.method == "POST":
            if StdEducational_Form.is_valid:
                StdEducational_Form = StdEducationalGoodForm(request.POST, instance=edu)
                try:
                    StdEducational_Form.save()
                except ValueError:
                    has_error = True
            
            return HttpResponseRedirect(reverse_lazy('manage-student', kwargs={'student_id': edu.student.pk}))    
        

        context={
            'educational': StdEducational_Form,
            'student_id': edu.student.pk,
            'type': "ویرایش",
            'text': "مثبت",
            'has_error': has_error
        }    
        return render(request, "accounts/manage-student-educational.html", context)
    
    else:
        raise Http404




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
