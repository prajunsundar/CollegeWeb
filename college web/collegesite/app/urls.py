from django.urls import path
from .views import index,admin_view,teacher_view,student_view,admin_signup_view,teacher_signup_view,student_signup_view
from . import views
from django.contrib.auth.views import LoginView,LogoutView
app_name='app'

urlpatterns=[
    path('',index,name='index'),
    path('admin-view',admin_view,name='admin-view'),
    path('teacher-view',teacher_view,name='teacher-view'),
    path('student-view',student_view,name='student-view'),

    path('admin-signup',admin_signup_view,name='admin-signup'),
    path('teacher-signup',teacher_signup_view,name='teacher-signup'),
    path('student-signup',student_signup_view,name='student-signup'),

    path('admin-login',LoginView.as_view(template_name='admin-login.html')),
    path('teacher-login',LoginView.as_view(template_name='teacher-login.html')),
    path('student-login',LoginView.as_view(template_name='student-login.html')),
    path('login-view',views.login_view,name='login-view'),
    path('logout',LogoutView.as_view(template_name='index.html'),name='logout'),


    path('admin-dashboard',views.admin_dashboard_view,name='admin_dash'),
    path('admin-teacher',views.admin_teacher_view,name='admin-teacher'),
    path('admin-teacher-add',views.admin_add_teacher_view,name='admin-teacher-add'),
    path('admin-teacher-view',views.admin_view_teacher_view,name='admin-teacher-view'),
    path('admin-teacher-approve',views.admin_approve_teacher_view,name='admin-teacher-approve'),
    path('teacher-approve/<int:pk>', views.approve_teacher_view, name='teacher-approve'),
    path('admin-teacher-cancel/<int:pk>', views.delete_teacher_view, name='admin-teacher-cancel'),
    path('admin-teacher-update/<int:pk>', views.admin_update_teacher_view, name='admin-teacher-update'),
    path('admin-teacher-delete/<int:pk>', views.delete_teacher_from_school_view, name='admin-teacher-delete'),
    path('admin-teacher-salary', views.admin_view_teacher_salary_view, name='admin-teacher-salary'),


    path('admin-student', views.admin_student_view, name='admin-student'),
    path('admin-student-view', views.admin_view_student_view, name='admin-student-view'),
    path('admin-student-add', views.admin_add_student_view, name='admin-student-add'),
    path('admin-student-approve', views.admin_approve_student_view, name='admin-student-approve'),
    path('student-approve/<int:pk>', views.approve_student, name='student-approve'),
    path('admin-student-cancel/<int:pk>', views.cancel_student_view, name='admin-student-cancel'),
    path('admin-student-update/<int:pk>', views.update_student_view, name='admin-student-update'),
    path('admin-student-delete/<int:pk>', views.delete_student_from_school_view, name='admin-student-delete'),

    path('admin-student-fee', views.admin_student_fee_view, name='admin-student-fee'),
    path('admin-notice-view', views.admin_notice_view, name='admin-notice'),

    path('admin-attendance', views.admin_attendance_view, name='admin-attendance'),
    path('admin-attendance-take/<str:cl>', views.admin_take_attendance_view, name='admin-attendance-take'),
    path('admin-attendance-view/<str:cl>', views.admin_view_attendance_view, name='admin-attendance-view'),







    path('teacher-dashboard',views.teacher_dashboard_view,name='teacher-dash'),
    path('teacher-student-view', views.teacher_view_student_view, name='teacher-student'),
    path('teacher-student-fees', views.teacher_student_fee_view, name='teacher-student-fees'),
    path('teacher-attendance', views.teacher_attendance_view, name='teacher-attendance'),
    path('teacher-attendance-take/<str:cl>', views.teacher_take_attendance_view, name='teacher-attendance-take'),
    path('teacher-attendance-view/<str:cl>', views.teacher_view_attendance_view, name='teacher-attendance-view'),
    path('teacher-notice-board', views.teacher_notice_view, name='teacher-notice'),

    path('student-dashboard', views.student_dashboard_view, name='student-dash'),
    path('student-attendance-view', views.student_attendance_view, name='student-attendance-view'),



]






