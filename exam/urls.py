from django.urls import path

from . import views

app_name = 'exam'
urlpatterns = [

    # ex: /exam/create/
    path('create/', views.create_exam, name='create_exam'),

    # ex: /exam/create/7/2/
    path('create/<int:exam_id>/<int:question_num>/', views.create_question, name='create_question'),

    # ex: /exam/title/
    path('<slug:slug>/', views.take_exam, name='take_exam'),

    # ex: /exam/result/
    path('<slug:slug>/result/', views.result, name="result"),

    path('<slug:slug>/scores/', views.scoreboard, name="scores"),
]