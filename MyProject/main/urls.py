# main/urls.py
from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.welcome, name='welcome'),              # Üdvözlő oldal
    path('personal/', views.personal, name='personal'),   # Személyes oldal
    path('download/', views.download_extension, name='download_extension'),  # Bővítmény letöltése oldal
    path('learn_more/', views.learn_more, name='learn_more'),  # Tudj meg többet oldal
    path('login/', CustomLoginView.as_view(), name='login'),   # Bejelentkezés oldal
    path('logout/', auth_views.LogoutView.as_view(next_page='welcome'), name='logout'),  # Kijelentkezés
    path('register/', views.register, name='register'),   # Regisztráció oldal
    path('upload_history_file/', views.upload_history_file, name='upload_history_file'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)