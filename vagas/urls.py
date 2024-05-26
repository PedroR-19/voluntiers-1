# vagas/urls.py
from django.urls import path

from . import views

app_name = 'vagas'

urlpatterns = [
    path('', views.vaga_list_view_home, name="home"),
    path('vagas/search/', views.VagaListViewSearch.as_view(), name="search"),
    path('vagas/category/<int:category_id>/', views.VagaListViewCategory.as_view(), name="category"),
    path('vagas/<int:pk>/', views.VagaDetail.as_view(), name="vaga"),
    path('vaga/<int:vaga_id>/candidatar/', views.candidatar_vaga, name='candidatar_vaga'),
]
