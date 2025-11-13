from django.urls import path
from . import views

urlpatterns = [
    # Homepage and information
    path('', views.home, name='home'),
    path('about/', views.about_ld, name='about_ld'),
    
    # Registration and authentication
    path('register/', views.register_choice, name='register_choice'),
    path('register/parent/', views.register_parent, name='register_parent'),
    path('register/teacher/', views.register_teacher, name='register_teacher'),
    path('register/psychologist/', views.register_psychologist, name='register_psychologist'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Testing functionality
    path('take-test/', views.take_test, name='take_test'),
    path('test/guidelines/', views.test_guidelines, name='test_guidelines'),
    path('test/child-info/', views.child_info, name='child_info'),
    path('test/questions/', views.test_questions, name='test_questions'),
    path('test/results/', views.test_results, name='test_results'),
    path('api/result-data/<int:result_id>/', views.get_result_data, name='get_result_data'),
]