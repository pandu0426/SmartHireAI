from django.urls import path
from . import views

urlpatterns = [
    path('<int:resume_id>/', views.chat_resume, name='chat_resume'),
]
