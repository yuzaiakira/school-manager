from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views import View

from information import models
from information import forms

from accounts.forms import UserForm


# Create your views here.

class FormSubmitStd(LoginRequiredMixin, View):
    login_url = settings.LOGIN_URL
    redirect_field_name = settings.REDIRECT_FIELD_NAME

    template_name = "accounts/submit_form_std.html"
    title = "مشخصات دانش آموز"
    warning_alert = None

    previous_page = None
    next_page = reverse_lazy("accounts:father")

    model = models.StdInfoModel
    form = forms.StdInfoForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        student_model, created = self.model.objects.get_or_create(user=request.user)

        context['student_form'] = self.form(instance=student_model)
        context['user_form'] = UserForm(instance=request.user)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if not request.user.editable:
            context['error'] = "زمان ویرایش فرم به اتمام رسیده شما دسترسی لازم را ندارید."

            student_model, created = self.model.objects.get_or_create(user=request.user)
            context['student_form'] = self.form(instance=student_model)
            context['user_form'] = UserForm(instance=request.user)

            return render(request, self.template_name, context)

        context['student_form'] = self.form(request.POST, instance=request.user.StdInfoModel)
        context['user_form'] = UserForm(request.POST, instance=request.user)

        if context['student_form'].is_valid() and context['user_form'].is_valid():
            try:
                context['student_form'].save()
                context['user_form'].save()
                context['success'] = "اطلاعات با موفقیت ثبت شده است لطفا به قرم بعدی بروید"
                render(request, self.template_name, context)
            except ValueError:
                context['error'] = "اطلاعات وارد شده تامعتبر میباشد"

            return render(request, self.template_name, context)

        context['error'] = "اطلاعات وارد شده تامعتبر میباشد"
        return render(request, self.template_name, context)

    def get_context_data(self):
        context = {
            'page_title': self.title,
            "warning_alert": self.warning_alert,
        }
        if self.next_page:
            context["next_page"] = self.next_page
        if self.previous_page:
            context["previous_page"] = self.previous_page

        return context



class FormSubmitFather(FormSubmitStd):
    title = "مشخصات پدر دانش آموز"
    template_name = "accounts/submit_form.html"

    model = models.FatherInfoModel
    form = forms.FatherInfoForm

    previous_page = reverse_lazy("accounts:profile")
    next_page = reverse_lazy("accounts:mother")

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        student_model, created = models.StdInfoModel.objects.get_or_create(user=request.user)
        form_model, created = self.model.objects.get_or_create(student=student_model)

        context['form'] = self.form(instance=form_model)

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        if not request.user.editable:
            context['error'] = "زمان ویرایش فرم به اتمام رسیده شما دسترسی لازم را ندارید."

            student_model, created = models.StdInfoModel.objects.get_or_create(user=request.user)
            form_model, created = self.model.objects.get_or_create(student=student_model)

            context['form'] = self.form(instance=form_model)
            return render(request, self.template_name, context)

        student_model, created = models.StdInfoModel.objects.get_or_create(user=request.user)
        form_model, created = self.model.objects.get_or_create(student=student_model)

        context['form'] = self.form(request.POST, instance=form_model)

        if context['form'].is_valid():
            try:
                context['form'].save()
                context['success'] = "اطلاعات با موفقیت ثبت شده است لطفا به قرم بعدی بروید"
                return render(request, self.template_name, context)
            except ValueError:
                context['error'] = "اطلاعات وارد شده تامعتبر میباشد"

            return render(request, self.template_name, context)

        return render(request, self.template_name, context)


class FormSubmitMother(FormSubmitFather):
    title = "مشخصات مادر دانش آموز"

    model = models.MatherInfoModel
    form = forms.MotherInfoForm

    previous_page = reverse_lazy("accounts:father")
    next_page = reverse_lazy("accounts:supervisor")


class FormSubmitSupervisor(FormSubmitFather):
    title = "مشخصات سرپرست دانش آموز"
    warning_alert = "در صورتی تکمیل شود که سرپرست دانش آموز به غیر از پدر یا مادر می باشد. در غیر این صوزت خالی بزارید"

    model = models.SupervisorInfoModel
    form = forms.SupervisorInfoForm

    previous_page = reverse_lazy("accounts:mother")
    next_page = reverse_lazy("accounts:lastschool")


class FormSubmitLastSchool(FormSubmitFather):
    title = "اطلاعات تحصیلی دانش آموز"

    model = models.StdLastSchoolModel
    form = forms.StdLastSchoolForm

    previous_page = reverse_lazy("accounts:supervisor")
    next_page = reverse_lazy("accounts:competitions")


class FormSubmitCompetitions(FormSubmitFather):
    title = "سابقه فعالیت های مسابقات"

    model = models.StdCompetitionsModel
    form = forms.StdCompetitionsForm

    previous_page = reverse_lazy("accounts:lastschool")
    next_page = reverse_lazy("accounts:shad")


class FormSubmitShad(FormSubmitFather):
    title = "مشخصات شاد دانش آموز"

    model = models.StdShadModel
    form = forms.StdShadForm

    previous_page = reverse_lazy("accounts:competitions")
    next_page = reverse_lazy("accounts:address")


class FormSubmitPlaceInfo(FormSubmitFather):
    title = "اطلاعات ارتباطی با دانش آموز"

    model = models.StdPlaceInfoModel
    form = forms.StdPlaceInfoForm

    previous_page = reverse_lazy("accounts:shad")
    next_page = None


