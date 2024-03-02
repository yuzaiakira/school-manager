from django.urls import path, include
from django.contrib.auth.views import LogoutView

from accounts import views
from azbankgateways.urls import az_bank_gateways_urls


app_name = "accounts"

urlpatterns = [
    path('', views.account_view, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=app_name+':login'), name='logout'),
    path('search/', views.StdList.as_view(), name='search'),

    path('form/', include('information.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('', include('payments.urls')),

    path('student/', include([
        path('',  views.StdList.as_view(), name='student'),
        path('<int:student_id>', views.manage_student_view, name='manage-student'),
        path('info/<int:student_id>', views.student_info_view, name='student-info'),
    ])),

    path('group/', include([
            path('', views.group_view, name='group'),
            path('upload/<int:group_id>', views.group_upload_view, name='group-upload'),
            ])),

    path('profile/', include([
        path('reset-password/', views.reset_password_view, name='reset-password'),
    ])),

]
