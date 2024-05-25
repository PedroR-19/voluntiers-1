# vagas/models.py

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=65)

    def __str__(self):
        return self.name


class Vaga(models.Model):
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField(unique=True)
    salary = models.IntegerField()
    types = models.CharField(max_length=65)
    requirements = models.TextField()
    requirements_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(
        upload_to='vagas/covers/%Y/%m/%d/', blank=True, default='')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        default=None,
    )
    profile = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('vagas:vaga', args=(self.id,))

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        return super().save(*args, **kwargs)


class Candidatura(models.Model):
    vaga = models.ForeignKey('Vaga', on_delete=models.CASCADE, related_name='candidaturas_vaga')
    candidato = models.ForeignKey(User, on_delete=models.CASCADE)
    curriculo = models.FileField(upload_to='curriculos/%Y/%m/%d/')
    data_candidatura = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.candidato.username} - {self.vaga.title}'
    