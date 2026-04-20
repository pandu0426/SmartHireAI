from django.urls import path
from . import views

urlpatterns = [
    path('<int:resume_id>/', views.chat_resume, name='chat_resume'),
    path('<int:resume_id>/ajax/', views.chat_ajax, name='chat_ajax'),
    path('<int:resume_id>/clear/', views.clear_chat, name='clear_chat'),
]
