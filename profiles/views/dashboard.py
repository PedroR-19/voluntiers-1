# profiles/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from vagas.models import Vaga, Candidatura
from profiles.models import Profile

@login_required
def dashboard(request):
    profile = request.user.profile

    # Inicializa o contexto com o perfil e o tipo de usuário
    context = {
        'profile': profile,
        'user_type': profile.user_type,
    }

    # Identifica o tipo de usuário e busca os dados correspondentes
    if profile.user_type == 'Voluntier':
        candidaturas = Candidatura.objects.filter(candidato=request.user)
        context['candidaturas'] = candidaturas
    else:
        vagas = Vaga.objects.filter(profile=request.user)
        context['vagas'] = vagas

    return render(request, 'profiles/pages/dashboard.html', context)
