from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy

from core.settings import REDIRECT_FIELD_NAME


class AddAndUpdateModel:
    model = None
    form = None
    template = None
    url_redirect = None
    add_text = "add"
    update_text = "update"

    @classmethod
    def _redirect(cls):
        return reverse_lazy(cls.url_redirect)

    @classmethod
    @login_required(None, REDIRECT_FIELD_NAME)
    def add_views(cls, request):
        if request.user.is_staff:
            context = dict()

            context['form'] = cls.form()
            context['type'] = cls.add_text
            context['back'] = cls._redirect()

            if request.method == "POST":
                if context['form'].is_valid:
                    context['new_model_obj'] = cls.model.objects.create()
                    context['form'] = cls.form(request.POST, instance=context['new_model_obj'])
                    try:
                        context['form'].save()
                    except ValueError:
                        context['has_error'] = True

                return HttpResponseRedirect(cls._redirect())

            return render(request, cls.template, context)

        else:
            return HttpResponseForbidden()

    @classmethod
    @login_required(None, REDIRECT_FIELD_NAME)
    def update_view(cls, request, pk):
        if request.user.is_staff:
            context = dict()

            context['model_obj'] = get_object_or_404(cls.model, pk=pk)
            context['payment_form'] = cls.form(instance=context['model_obj'])
            context['type'] = cls.update_text
            context['back'] = cls._redirect()

            if request.method == "POST":
                if context['payment_form'].is_valid:

                    context['payment_form'] = cls.form(request.POST, instance=context['model_obj'])
                    try:
                        context['payment_form'].save()
                    except ValueError:
                        context['has_error'] = True

                return HttpResponseRedirect(cls._redirect())

            return render(request, cls.template, context)

        else:
            return HttpResponseForbidden()
