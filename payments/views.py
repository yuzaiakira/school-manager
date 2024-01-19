from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy, reverse

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import DeleteView

import logging
import jdatetime

from core.settings import REDIRECT_FIELD_NAME

from azbankgateways import bankfactories, models as bank_models, default_settings as settings
from azbankgateways.exceptions import AZBankGatewaysException

from payments.models import UserPriceModel, UserPaymentModel
from payments.forms import UserPriceForm, UserPaymentForm
from payments.functions import check_part_of_installment, get_total_price, price_peer_part

from accounts.models import UserModel
from information.models import StdInfoModel

# Create your views here.


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def user_price_create_view(request, std_id):
    if request.user.is_staff:
        context = dict()

        context['user'] = get_object_or_404(UserModel, pk=std_id)
        context['user_price_form'] = UserPriceForm()
        context['text'] = "افزودن"
        context['can_delete'] = False
        context['back'] = context['user'].StdInfoModel.pk

        if request.method == "POST":
            if context['user_price_form'].is_valid:
                context['user_price'] = UserPriceModel.objects.create(user=context['user'])
                context['user_price_form'] = UserPriceForm(request.POST, instance=context['user_price'])
                try:
                    context['user_price_form'].save()
                except ValueError:
                    context['has_error'] = True

            return HttpResponseRedirect(reverse_lazy('manage-student',
                                                     kwargs={'student_id': context['user'].StdInfoModel.pk}))

        return render(request, "payments/user-price-update.html", context)

    else:
        raise Http404


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def user_price_update_view(request, pk):
    if request.user.is_staff:
        context = dict()

        context['price'] = get_object_or_404(UserPriceModel, pk=pk)
        context['user_price_form'] = UserPriceForm(instance=context['price'])
        context['text'] = "ویرایش"
        context['can_delete'] = pk
        context['back'] = context['price'].user.StdInfoModel.pk

        if request.method == "POST":
            if context['user_price_form'].is_valid:

                context['user_price_form'] = UserPriceForm(request.POST, instance=context['price'])
                try:
                    context['user_price_form'].save()
                except ValueError:
                    context['has_error'] = True

            return HttpResponseRedirect(reverse_lazy('manage-student',
                                                     kwargs={'student_id': context['price'].user.StdInfoModel.pk}))

        return render(request, "payments/user-price-update.html", context)

    else:
        raise Http404


class UserPriceDelete(DeleteView):
    model = UserPriceModel
    context_object_name = 'user_price'

    def form_valid(self, form):
        messages.success(self.request, "The report was deleted successfully.")
        return super(UserPriceDelete, self).form_valid(form)

    def get_success_url(self):
        std_object = self.get_object()
        std_id = std_object.user.StdInfoModel.pk
        return reverse_lazy('manage-student', kwargs={'student_id': std_id})


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def payment_details_view(request, pay_id):
    if request.user.is_staff:
        context = dict()

        context['total'] = get_object_or_404(UserPriceModel, pk=pay_id)
        context['info'] = get_object_or_404(StdInfoModel, pk=context['total'].user.StdInfoModel.pk)
        context['History'] = UserPaymentModel.objects.filter(total=context['total'])
        context['pays'] = get_total_price(context['History'])
        context['parts'] = check_part_of_installment(context['total'])
        context['over'] = context['total'].total_price.price - context['pays']

        return render(request, "payments/payment-details.html", context)

    else:
        raise Http404


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def payment_details_update_view(request, payment_id):
    if request.user.is_staff:
        context = dict()

        context['payment'] = get_object_or_404(UserPaymentModel, pk=payment_id)
        context['payment_form'] = UserPaymentForm(instance=context['payment'])
        context['text'] = "ویرایش"
        context['can_delete'] = True
        context['back'] = context['payment'].total.pk

        if request.method == "POST":
            if context['payment_form'].is_valid:

                context['payment_form'] = UserPaymentForm(request.POST, instance=context['payment'])
                try:
                    context['payment_form'].save()
                except ValueError:
                    context['has_error'] = True

            return HttpResponseRedirect(reverse_lazy('payment-details', kwargs={'pay_id': context['payment'].total.pk}))

        return render(request, "payments/payment-details-update.html", context)

    else:
        raise Http404


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def payment_details_create_view(request, pay_id):
    if request.user.is_staff:
        context = dict()

        context['total'] = get_object_or_404(UserPriceModel, pk=pay_id)
        context['payment_form'] = UserPaymentForm()
        context['text'] = "افزودن"
        context['back'] = pay_id

        if request.method == "POST":
            if context['payment_form'].is_valid:
                context['payment'] = UserPaymentModel.objects.create(total=context['total'])
                context['payment_form'] = UserPaymentForm(request.POST, instance=context['payment'])
                try:
                    context['payment_form'].save()
                except ValueError:
                    context['has_error'] = True

            return HttpResponseRedirect(reverse_lazy('payment-details', kwargs={'pay_id': pay_id}))

        return render(request, "payments/payment-details-update.html", context)

    else:
        raise Http404


class PaymentDelete(DeleteView):
    model = UserPaymentModel
    context_object_name = 'payment'

    def form_valid(self, form):
        messages.success(self.request, "The report was deleted successfully.")
        return super(PaymentDelete, self).form_valid(form)

    def get_success_url(self):
        pay_object = self.get_object()
        payment_id = pay_object.total.pk
        return reverse_lazy('payment-details', kwargs={'pay_id': payment_id})


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def user_payment_show_view(request):
    context = dict()
    context['total'] = UserPriceModel.objects.filter(user=request.user)
    for total_price in context['total']:
        if  not price_peer_part(total_price):
            total_price.finished = True
            total_price.save
    return render(request, "payments/user-payment-show.html", context)


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def user_payment_price_view(request, pk):
    context = dict()
    context['total'] = get_object_or_404(UserPriceModel, pk=pk)
    if context['total'].user == request.user:

        context['History'] = UserPaymentModel.objects.filter(total=context['total'])
        context['pays'] = get_total_price(context['History'])
        context['parts'] = check_part_of_installment(context['total'])
        context['over'] = context['total'].total_price.price - context['pays']
        context['can_payemet'] = price_peer_part(context['total'])

        return render(request, "payments/user-payment-price.html", context)
    else:
        raise Http404()


@login_required(redirect_field_name=REDIRECT_FIELD_NAME)
def go_to_gateway_view(request, pk):
    context = dict()
    context['total'] = get_object_or_404(UserPriceModel, pk=pk)
    if context['total'].user == request.user:
        amount = price_peer_part(context['total'])

        if amount <= 0:
            context = {
                'title': "مبلغ نامعتبر",
                'des': "شهریه شما به طور کامل پرداخت شده است و یا مبلغ درخواستی نا معتبر میباشد"
            }
            return render(request, 'payments/payment-error-page.html', context)

        factory = bankfactories.BankFactory()
        try:
            bank = factory.auto_create()
            bank.set_request(request)
            bank.set_amount(amount)

            bank.set_client_callback_url(reverse('callback-gateway', kwargs={'pk':pk}))

            bank_record = bank.ready()


            return bank.redirect_gateway()
        except AZBankGatewaysException as e:
            logging.critical(e)
            # TODO: redirect to failed page.
            raise e

    else:
        raise Http404()


def callback_gateway_view(request, pk):
    tracking_code = request.GET.get(settings.TRACKING_CODE_QUERY_PARAM, None)
    if not tracking_code:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    try:
        bank_record = bank_models.Bank.objects.get(tracking_code=tracking_code)
    except bank_models.Bank.DoesNotExist:
        logging.debug("این لینک معتبر نیست.")
        raise Http404

    # در این قسمت باید از طریق داده هایی که در بانک رکورد وجود دارد، رکورد متناظر یا هر اقدام مقتضی دیگر را انجام دهیم
    if bank_record.is_success:
        try:
            total_price = UserPriceModel.objects.get(pk=pk)
        except UserPriceModel.DoesNotExist:
            context = {
                'title': "شهریه ناموجود",
                'des': "شهریه ای که پرداخت کردید نامعتبر میباشد، لطفا با مدیریت تماس بگیرید"
            }
            return render(request, 'payments/payment-error-page.html', context)

        obj = UserPaymentModel.objects.create(total=total_price,
                                              price=price_peer_part(total_price),
                                              description="پرداخت توسط درگاه پرداخت آنلاین",
                                              date=jdatetime.datetime.now())

        factory = bankfactories.BankFactory()
        bank_models.Bank.objects.update_expire_records()

        for item in bank_models.Bank.objects.filter_return_from_bank():
            bank = factory.create(bank_type=item.bank_type, identifier=item.bank_choose_identifier)
            bank.verify(item.tracking_code)
            bank_record = bank_models.Bank.objects.get(tracking_code=item.tracking_code)
            if bank_record.is_success:
                logging.debug("This record is verify now.", extra={'pk': bank_record.pk})

        try:
            obj.save()
        except:
            context = {
                'title': "مشکل در ذخیره سازی",
                'des': "مشکلی در ذخیره اطلاعات پیش آمده است لطفا با مدیریت تماس بگیرید"
            }
            return render(request, 'payments/payment-error-page.html', context)

        return HttpResponseRedirect(reverse('add-user-payment', kwargs={'pk':pk}))

    # پرداخت موفق نبوده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت.
    context = {
        'title': "پرداخت با شکست مواجه شده است.",
        'des':"پرداخت با شکست مواجه شده است. اگر پول کم شده است ظرف مدت ۴۸ ساعت پول به حساب شما بازخواهد گشت."
    }
    return render(request, 'payments/payment-error-page.html', context)

def hi(request):
    context = {
        'title': "فثسف",
        'des':"None"
    }
    return render(request, 'payments/payment-error-page.html', context)
