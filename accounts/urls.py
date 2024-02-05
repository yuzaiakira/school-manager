from django.urls import path, include
from django.contrib.admin.views.decorators import staff_member_required
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
        path('', views.student_view, name='student'),
        path('<int:student_id>', views.manage_student_view, name='manage-student'),
        path('info/<int:student_id>', views.student_info_view, name='student-info'),

        path('report/', include([
            path('create/<int:student_id>', views.report_create_view, name='report-create'),
            path('delete/<int:pk>/', staff_member_required(views.ReportDelete.as_view(), login_url='login'),
                 name='report-delete'),
            path('update/<int:report_id>/', views.report_update_view, name='report-update'),
            ])),

        path('edu/', include([
            path('create/good/<int:student_id>', views.Educational_good_create_view, name='edu-good-create'),
            path('update/good/<int:edu_id>', views.Educational_good_update_view, name='edu-good-update'),
            path('create/bad/<int:student_id>', views.Educational_bad_create_view, name='edu-bad-create'),
            path('update/bad/<int:edu_id>', views.Educational_bad_update_view, name='edu-bad-update'),
            path('delete/<int:pk>', staff_member_required(views.EducationalDelete.as_view(),
                                                          login_url='login'), name='edu-delete'),
            ])),

    ])),

    path('group/', include([
            path('', views.group_view, name='group'),
            path('upload/<int:group_id>', views.group_upload_view, name='group-upload'),
            ])),

    path('profile/', include([
        path('reset-password/', views.reset_password_view, name='reset-password'),
    ])),

]
