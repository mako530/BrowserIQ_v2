import os

from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from .ai_recommender import recommend_content


def welcome(request):
    return render(request, 'welcome.html')


def download_extension(request):
    return render(request, 'download.html')

def learn_more(request):
    return render(request, 'learn_more.html')


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


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SearchHistory


@csrf_exempt
def upload_history_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            urls = data.get('urls', [])
            user = request.user  # vagy más módon azonosíthatjuk a felhasználót

            for url in urls:
                SearchHistory.objects.create(user=user, url=url)

            return JsonResponse({"status": "success", "message": "Előzmények sikeresen mentve!"})
        except Exception as e:
            print("Hiba történt:", e)
            return JsonResponse({"status": "error", "message": "Hiba történt az előzmények mentése során."}, status=500)
    return JsonResponse({"status": "error", "message": "Csak POST kérés fogadható!"}, status=400)

@login_required
def personal_view(request):
    # Felhasználói előzmények lekérése
    user_history = [history.url for history in SearchHistory.objects.filter(user=request.user)]

    # Ajánlások generálása
    recommendations = recommend_content(user_history)

    # Statisztikák (például kedvelt oldalak és érdeklődési körök)
    stats = {
        "favourite_sites_count": len(user_history),  # példaként összes URL
        "interests": "Technológia, Tudomány"  # statikus adat példaként
    }

    # Feltöltött fájlok listázása
    uploaded_files = SearchHistory.objects.filter(user=request.user)

    return render(request, "personal.html", {
        "recommendations": recommendations,
        "stats": stats,
        "uploaded_files": uploaded_files
    })