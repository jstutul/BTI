from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.urls import path
from .views import *

app_name = 'dashboard'

urlpatterns = [
    path('admin/', admin_dashboard,name="admin_dashboard"),
    path('institution/', institution_dashboard,name="institution_dashboard"),
    path('student/', student_dashboard,name="student_dashboard"),

    # Admin 
    path('admin/courses/', course_list, name='course_list'),
    path('admin/courses/add/', course_add, name='course_add'),
    path('admin/courses/<int:pk>/edit/', course_edit, name='course_edit'),
    path('admin/courses/<int:pk>/delete/', course_delete, name='course_delete'),

    path('admin/sessions/add/', session_add, name='session_add'),
    path('admin/sessions/<int:pk>/edit/', session_edit, name='session_edit'),
    path('admin/sessions/<int:pk>/delete/', session_delete, name='session_delete'),

    path('admin/institutions/', institution_list, name='institution_list'),
    path('admin/institutions/add/', institution_add, name='institution_add'),
    path('admin/institutions/<int:pk>/edit/', institution_edit, name='institution_edit'),
    path('admin/institutions/<int:pk>/delete/', institution_delete, name='institution_delete'),

    # Admin & Institution 
    path('students/', student_list, name='student_list'),
    path('students/add/', student_add, name='student_add'),
    path('students/<int:pk>/edit/', student_edit, name='student_edit'),
    path('students/<int:pk>/toggle/', student_toggle, name='student_toggle'),
    path('students/<int:student_id>/assign/', assign_course, name='assign_course'),

    path('results/', result_list, name='result_list'),
    path('results/add/', result_add, name='result_add'),
    path('results/<int:pk>/edit/', result_edit, name='result_edit'),

    path('certificate/delete/<int:pk>/', certificate_delete, name='certificate_delete'),
    path('certificate/', certificate_list, name='certificate_list'),
    path('certificate/edit/<int:pk>/', certificate_edit, name='certificate_edit'),
    path('certificate/generate/', certificate_generate, name='certificate_generate'),
    path('result/info/<int:pk>/', get_result_info, name='result_info'),
    path('certificate/content/<int:pk>/', certificate_html_api, name='certificate_html_api'),

    path('deposit/', deposit_page, name='deposit_page'),
    path("deposit/pay/", bkash_pay, name="bkash_pay"),
    path("deposit/callback/", bkash_callback, name="bkash_callback"),
    path("transactions/", transaction_list, name="transactions"),

]
