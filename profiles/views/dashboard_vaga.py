from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from profiles.forms.vaga_form import ProfileVagaForm
from vagas.models import Vaga


@method_decorator(
    login_required(login_url='profiles:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardVaga(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup(self, *args, **kwargs):
        return super().setup(*args, **kwargs)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_vaga(self, id=None):
        vaga = None

        if id is not None:
            vaga = Vaga.objects.filter(
                profile=self.request.user,
                pk=id,
            ).first()

            if not vaga:
                raise Http404()

        return vaga

    def render_vaga(self, form):
        return render(
            self.request,
            'profiles/pages/dashboard_vaga.html',
            context={
                'form': form
            }
        )

    def get(self, request, id=None):
        vaga = self.get_vaga(id)
        form = ProfileVagaForm(instance=vaga)
        return self.render_vaga(form)

    def post(self, request, id=None):
        vaga = self.get_vaga(id)
        form = ProfileVagaForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=vaga
        )

        if form.is_valid():
            # Agora, o form é válido e eu posso tentar salvar
            vaga = form.save(commit=False)

            vaga.profile = request.user
            vaga.requirements_is_html = False

            vaga.save()

            messages.success(request, 'Sua vaga foi salva com sucesso!')
            return redirect(
                reverse(
                    'profiles:dashboard_vaga_edit', args=(
                        vaga.id,
                    )
                )
            )

        return self.render_vaga(form)


@method_decorator(
    login_required(login_url='profiles:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardVagaDelete(DashboardVaga):
    def post(self, *args, **kwargs):
        vaga = self.get_vaga(self.request.POST.get('id'))
        vaga.delete()
        messages.success(self.request, 'Deleted successfully.')
        return redirect(reverse('profiles:dashboard'))
