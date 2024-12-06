# main/urls.py
from django.urls import path
from . import views
from .views import CustomLoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome, name='welcome'),              # Üdvözlő oldal
    path('personal/', views.personal_view, name='personal'),   # Személyes oldal
    path('download/', views.download_extension, name='download_extension'),  # Bővítmény letöltése oldal
    path('learn_more/', views.learn_more, name='learn_more'),  # Tudj meg többet oldal
    path('login/', CustomLoginView.as_view(), name='login'),   # Bejelentkezés oldal
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),   # Regisztráció oldal
    path('upload_history/', views.upload_history_file, name='upload_history'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)