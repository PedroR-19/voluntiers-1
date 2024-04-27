from django.db.models import Q
from django.http.response import Http404
from django.views.generic import DetailView, ListView

from vagas.models import Vaga
from utils.pagination import make_pagination

PER_PAGE = 6


class VagaListViewBase(ListView):
    model = Vaga
    context_object_name = 'vagas'
    ordering = ['-id']
    template_name = 'vagas/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
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


class VagaListViewHome(VagaListViewBase):
    template_name = 'vagas/pages/home.html'


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
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx
