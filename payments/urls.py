from django.urls import path, include
from django.contrib.admin.views.decorators import staff_member_required
from payments import views


urlpatterns = [
    path('price/', include([
        path('<int:std_id>/add/', views.user_price_create_view, name='user-price-add'),
        path('<int:pk>/update/', views.user_price_update_view, name='user-price-update'),
        path('<int:pk>/delete/', staff_member_required(views.UserPriceDelete.as_view(), login_url='login'),
             name='user-price-delete'),
    ])),

    path('payment/', include([
        path('<int:pay_id>', views.payment_details_view, name='payment-details'),
        path('<int:payment_id>/update', views.payment_details_update_view, name='payment-details-update'),
        path('<int:pay_id>/add', views.payment_details_create_view, name='payment-details-add'),
        path('<int:pk>/delete', staff_member_required(views.PaymentDelete.as_view(), login_url='login'),
             name='payment-details-delete')
    ])),

    path('user-payment/', include([
        path('', views.user_payment_show_view, name='user-payment-details'),
        path('<int:pk>', views.user_payment_price_view, name='user-payment-price'),
    ])),
    # TODO: add /  end of all url
    path('add-payment/<int:pk>', views.user_payment_price_view, name='add-user-payment'),
    path('go-to-gateway/<int:pk>', views.go_to_gateway_view, name='go-to-gateway'),
    path('callback-gateway/<int:pk>', views.callback_gateway_view, name='callback-gateway'),
    path('test', views.hi),

]
