from django.urls import path,include
from .views import *


urlpatterns=[
    path('top/',top,name='top'),
    path('signup/',signup,name='signup'),
    path('signup_success/',signup_success,name="signup_success"),
    path('loginview/',loginview,name='loginview'),
    path('home/',home,name='home'),
    path('question/',question,name='question'),
    path('answer/<int:ans>',answer,name="answer"),
    path('result/',result,name="result"),
    path('logoutview/',logoutview,name="logoutview"),
    path('logout_success/',logout_success,name="logout_success"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('userdata/',user_data,name="userdata"),
    path('ranking/',ranking,name='ranking'),
    path('level_choice/',level_choice,name='level_choice'),
    path('quiz_start/<int:level>',quiz_start,name='quiz_start'),
    path('question_form/',question_form,name='question_form'),
    path('question_form_success/',question_form_success,name="form_success"),
    path('dbms/',dbms,name="dbms"),
    path('question_delete_form/',question_delete_form,name='question_delete_form'),
    path('delete_success/',delete_success,name='delete_success'),
    path('user_delete_form/',user_delete_form,name='user_delete_form'),
    path('user_delete_success/',user_delete_success,name='user_delete_success'),
]