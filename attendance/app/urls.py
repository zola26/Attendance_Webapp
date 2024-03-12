from django.urls import path
from app import views
from .views import update_detected_person_image
from .views import generate_student_report
from .views import send_all_reports
from .views import add_student
urlpatterns = [
    path('',views.home, name='home'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('logout_admin/', views.logout_admin, name='logout_admin'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('add-student/', add_student, name='add_student'),
    path('update-student/<int:student_id>/', views.update_student, name='update_student'),
    path('students_list/', views.student_list, name='students_list'),
    path('view_report/', views.view_report, name='view_report'),
    path('index/',views.index, name='index'),
    path('video_feed/', views.video_feed, name='video_feed'),
    # path('connect_webcam/', views.connect_webcam, name='connect_webcam'),
    # path('cam_connect/', views.cam_connect, name='cam_connect'),
    path('update_detected_person_image/', update_detected_person_image, name='update_detected_person_image'),
    path('generate_report/<int:student_id>/', generate_student_report, name='generate_student_report'),
    path('send_all_reports/', send_all_reports, name='send_all_reports'),
    path('sent_success/', views.sent_success, name='sent_success'),
    
]