from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_student, name='register_student'),
    path('home/', views.home, name='home'),
    path('create/', views.create_student, name='create_student'),
    path('edit/<int:pk>/', views.edit_student, name='edit_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('report/<int:pk>/', views.student_report, name='student_report'),
    path('marks/<int:pk>/', views.add_marks, name='add_marks'),
    path('achievement/<int:pk>/', views.add_achievement, name='add_achievement'),
    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('events/', views.manage_events, name='manage_events'),
    path('notifications/', views.manage_notifications, name='manage_notifications'),
    path('holidays/', views.manage_holidays, name='manage_holidays'),
    path('best-student/', views.best_student, name='best_student'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('feedbacks/', views.manage_feedbacks, name='manage_feedbacks'),
    path('registrations/', views.manage_registrations, name='manage_registrations'),
    path('subjects/', views.manage_subjects, name='manage_subjects'),
    path('parent/', views.parent_portal, name='parent_portal'),
]
