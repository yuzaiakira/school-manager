from django.urls import path, include
from django.contrib.auth.views import LogoutView

from accounts import views
from azbankgateways.urls import az_bank_gateways_urls


app_name = "accounts"

urlpatterns = [
    path('', views.HomeAccount.as_view(), name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page=app_name+':login'), name='logout'),
    path('search/', views.StdList.as_view(), name='search'),

    path('form/', include('information.urls')),
    path('bankgateways/', az_bank_gateways_urls()),
    path('', include('payments.urls')),

    path('student/', include([
        path('',  views.StdList.as_view(), name='student'),
        path('<int:student_id>', views.ManageStudents.as_view(), name='manage-student'),
        path('info/<int:student_id>', views.StudentInfo.as_view(), name='student-info'),
    ])),

    path('group/', include([
            path('', views.GroupList.as_view(), name='group'),
            path('upload/<int:group_id>', views.GroupUpload.as_view(), name='group-upload'),
            ])),

    path('profile/', include([
        path('reset-password/', views.ResetPassword.as_view(), name='reset-password'),
    ])),



]
