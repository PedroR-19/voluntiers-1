from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from profiles.forms import LoginForm, RegisterForm
from profiles.models import Profile
from vagas.models import Vaga, Candidatura


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'profiles/pages/register_view.html', {
        'form': form,
        'form_action': reverse('profiles:register_create'),
    })


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        profile = Profile.objects.create(user_id=user.id,
                                         user_type=form.cleaned_data['user_type'])
        profile.save()
        messages.success(request, 'Seu usuário foi criado, por favor faça login.')

        del (request.session['register_form_data'])
        return redirect(reverse('profiles:login'))

    return redirect('profiles:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'profiles/pages/login.html', {
        'form': form,
        'form_action': reverse('profiles:login_create')
    })


def login_create(request):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Você fez login!')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Credenciais inválidas')
    else:
        messages.error(request, 'Nome de usuário ou senha inválidos')

    return redirect(reverse('profiles:dashboard'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        messages.error(request, 'Requisição de logout inválida')
        return redirect(reverse('profiles:login'))

    if request.POST.get('username') != request.user.username:
        messages.error(request, 'Invalid logout user')
        return redirect(reverse('profiles:login'))

    messages.success(request, 'Logout feito com sucesso')
    logout(request)
    return redirect(reverse('profiles:login'))


@login_required(login_url='profiles:login', redirect_field_name='next')
def dashboard(request):
    user = request.user
    profile = request.user.profile
    if not request.user.is_superuser:
        profile = Profile.objects.get(user_id=request.user.id)
    if profile.user_type == 'Voluntier':
        candidaturas = Candidatura.objects.filter(
            candidato=request.user
        )
        return render(
            request,
            'profiles/pages/dashboard.html',
            context={
                'candidaturas': candidaturas,
                'user_type': profile.user_type,
                'user': request.user,
                'profile': profile
            }
        )
    else:
        vagas = Vaga.objects.filter(
            profile=request.user
        )
        return render(
            request,
            'profiles/pages/dashboard.html',
            context={
                'vagas': vagas,
                'user_type': profile.user_type,
                'user': request.user,
                'profile': profile
            }
        )