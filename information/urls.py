from django.urls import path
from information import views

urlpatterns = [
    path('', views.FormSubmitStd.as_view(), name='profile'),
    path('father/', views.FormSubmitFather.as_view(), name='father'),
    path('mother/', views.FormSubmitMother.as_view(), name='mother'),
    path('supervisor/', views.FormSubmitSupervisor.as_view(), name='supervisor'),
    path('lastschool/', views.FormSubmitLastSchool.as_view(), name='lastschool'),
    path('competitions/', views.FormSubmitCompetitions.as_view(), name='competitions'),
    path('shad/', views.FormSubmitShad.as_view(), name='shad'),
    path('address/', views.FormSubmitPlaceInfo.as_view(), name='address'),

]
