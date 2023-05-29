from django.urls import path
from Teachers import views
from .views import *


urlpatterns = [
    path('',views.index,name='home'),
    # path('login',views.loginuser,name="login"),
    # path('questions',views.questions,name="questions"),
    # path('logout',views.logoutuser,name="logout"),
    path('generate_pdf',views.generate_pdf,name="generate_pdf"),
    path("upload-image/", upload_image, name="upload-image"),
    path("success/", success, name="success"),
    path("omr/", views.omr, name="omr"),
    path("omr_gen_dow/<str:center_code>/<str:Exam_name>/<str:classes>/<str:subject>", views.omr_gen_dow, name="omr_gen_dow"),
    path('search/<str:exam_center>/<str:Exam_name>/<str:classes>/<str:subject>', views.search_results, name='search_results'),
    path('search/', views.search, name='search'),
    path('add_data', views.add_data, name='add_data'),
    path('upload/', upload_file, name='upload_file'),
    path('upload/<str:exam_center>/<str:exam_name>/<str:classes>/<str:subject>', views.upload_file, name='upload_file'),



    # path('save_exam_score/', views.save_exam_score, name='save_exam_score'),



    # ___________________LOGIN & LOGOUT & SIGNUP___________________________
    path('signup/',views.sign_up,name='teacherssignup'),
    path('login/',views.teachers_login,name='teacherslogin'),
    path('logout/',views.teachers_logout,name='logout'),
    # ______________________________________________



    # ________________OMR ULOAD and PROCESSING____________________________  
    path("scan_download/", views.scan_download, name="scan_download"),
    path('scan_search/', views.scan_search, name='scan_search'),
    # path("omr_scan_dow/<str:student_id>/<str:classes>/<str:subject>", views.omr_scan_dow, name="omr_scan_dow"),
    # path('search_scan_down/', views.upload_file, name='upload_file'),
    path('scan_search/<str:exam_center>/<str:exam_name>/<str:classes>/<str:subject>', views.scan_search_results, name='rrr'),

    
    
    
    

    # ______________________________________________
    path("view_results/", views.view_results, name="view_results"),
    path('view_results_search/', views.view_results_search, name='view_results_search'),
    path('view_results_search/<str:exam_center>/<str:exam_name>/<str:classes>/<str:subject>', views.results, name='results'),
    path('download_excel/<str:exam_center>/<str:exam_name>/<str:classes>/<str:subject>', views.download_excel, name='download_excel'),
    
   
   
   
    
# /logs/0002/final/12/sanskrit/Baban

    path('logs/<str:exam_code>/<str:Exam_name>/<str:Class>/<str:Subject>/<str:Name>', views.log, name='log'),


    
    
    
    
    

]



