from django.db.models import Q
from django.http.response import Http404
from django.views.generic import DetailView, ListView

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from vagas.models import Vaga, Candidatura
from vagas.forms import CandidaturaForm

from profiles.models import Profile
from vagas.models import Vaga
from .pagination import make_pagination

PER_PAGE = 6


class VagaListViewBase(ListView):
    model = Vaga
    context_object_name = 'vagas'
    ordering = ['-id']
    template_name = 'vagas/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('vagas'),
            PER_PAGE
        )
        ctx.update(
            {'vagas': page_obj, 'pagination_range': pagination_range}
        )
        return ctx


def vaga_list_view_home(request):
    user = request.user
    vagas = Vaga.objects.all(
    )

    if user.is_authenticated:
        profile = None
        if not user.is_superuser:
            profile = get_object_or_404(Profile, user_id=user.id)

        return render(
            request,
            'vagas/pages/home.html',
            context={
                'user': user,
                'profile': profile,
                'vagas': vagas,
            }
        )
    else:
        return render(
            request,
            'vagas/pages/home.html',
            context={
                'vagas': vagas,
            }
        )



class VagaListViewCategory(VagaListViewBase):
    template_name = 'vagas/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'title': f'{ctx.get("vagas")[0].category.name} - Category | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs


class VagaListViewSearch(VagaListViewBase):
    template_name = 'vagas/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class VagaDetail(DetailView):
    model = Vaga
    context_object_name = 'vaga'
    template_name = 'vagas/pages/vaga-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from vagas.models import Vaga
from vagas.forms import CandidaturaForm

@login_required
def candidatar_vaga(request, vaga_id):
    vaga = get_object_or_404(Vaga, id=vaga_id)
    if request.method == 'POST':
        form = CandidaturaForm(request.POST, request.FILES)
        if form.is_valid():
            candidatura = form.save(commit=False)
            candidatura.vaga = vaga
            candidatura.candidato = request.user
            candidatura.save()
            messages.success(request, 'Sua candidatura foi enviada!')
            return redirect('profiles:dashboard')
    else:
        form = CandidaturaForm()
    return render(request, 'vagas/pages/candidatar_vaga.html', {'form': form, 'vaga': vaga})

