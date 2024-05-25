# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from vagas.models import Candidatura, Vaga

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.user_type == 'ONG':
        vagas = Vaga.objects.filter(ong=request.user)
        return render(request, 'profiles/pages/dashboard.html', {'vagas': vagas, 'profile': profile})
    elif profile.user_type == 'Voluntier':
        candidaturas = Candidatura.objects.filter(candidato=request.user)
        return render(request, 'profiles/pages/dashboard.html', {'candidaturas': candidaturas, 'profile': profile})
    else:
        return render(request, 'profiles/pages/dashboard.html', {'profile': profile})
