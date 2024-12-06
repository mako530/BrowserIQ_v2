import os

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from dotenv import load_dotenv
from .ai_recommender import recommend_content
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import UserHistory

def welcome(request):
    return render(request, 'welcome.html')

def download_extension(request):
    return render(request, 'download.html')

def learn_more(request):
    return render(request, 'learn_more.html')

def custom_logout(request):
    logout(request)  # A felhasználó kijelentkeztetése
    return redirect('welcome')  # Átirányítás a 'welcome' oldalra

class CustomLoginView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('personal')

    def form_invalid(self, form):
        messages.error(self.request, 'Sikertelen bejelentkezés. Ellenőrizze a felhasználónevet és a jelszót.')
        return super().form_invalid(form)

@login_required
def personal(request):
    return render(request, 'personal.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Próbáljuk meg hitelesíteni a felhasználót regisztráció után
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Sikeres regisztráció és automatikus bejelentkezés!')
                return redirect('personal')  # Átirányítás a személyes oldalra
            else:
                messages.error(request, 'A hitelesítés nem sikerült. Próbálj meg manuálisan bejelentkezni.')
                return redirect('login')  # Ha a hitelesítés nem sikerül, vissza a bejelentkezésre
        else:
            messages.error(request, 'Hiba történt a regisztráció során. Próbáld újra.')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@csrf_exempt
def upload_history_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            urls = data.get('urls', [])
            print(data)
            if not urls:
                return JsonResponse({"status": "error", "message": "No URLs provided"}, status=400)

            # Bejelentkezett felhasználó lekérése
            user = request.user
            print(user)
            if not user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User not authenticated"}, status=403)

            # URL-ek mentése
            for url in urls:
                UserHistory.objects.create(user=user, url=url)

            return JsonResponse({"status": "success", "message": "History saved successfully!"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)


load_dotenv()

@login_required
def personal_view(request):
    """
    A felhasználó keresési előzményei alapján ajánlások generálása.
    """
    user = request.user

    # Lekérjük a felhasználó URL előzményeit az adatbázisból
    search_history = UserHistory.objects.filter(user=user).values_list("url", flat=True)

    if not search_history:
        recommendations = {"message": "Nincsenek keresési előzményeid."}
    else:
        # Ajánlások generálása az URL-ek alapján
        recommendations = recommend_content(list(search_history))  # Konvertáld listára, ha QuerySet

    return render(request, "personal.html", {
        "recommendations": recommendations
    })
