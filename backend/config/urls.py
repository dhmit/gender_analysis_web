"""
URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL configuration
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from app import views


urlpatterns = [
    # Django admin page
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/example/<int:example_id>', views.get_example),
    path('api/all_documents', views.all_documents),
    path('api/add_document', views.add_document),
    path('api/document/<int:doc_id>', views.get_document),
    path('api/all_genders', views.all_genders),
    path('api/gender/<int:gender_id>', views.get_gender),
    path('api/add_gender', views.add_gender),
    path('api/delete_gender', views.delete_gender),
    path('api/all_pronoun_series', views.all_pronoun_series),
    path('api/pronoun_series/<int:pronoun_series_id>', views.get_pronoun_series),
    path('api/all_corpora', views.all_corpora),
    path('api/add_corpus', views.add_corpus),
    path('api/update_corpus_docs', views.update_corpus_docs),
    path('api/delete_corpus', views.delete_corpus),
    path('api/corpus/<int:corpus_id>', views.get_corpus),

    # View paths
    path('', views.index, name='index'),
    path('example', views.example, name='example'),
    path('example/<int:example_id>', views.example_id, name='example_id'),
    path('documents', views.documents, name='documents'),
    path('document/<int:doc_id>', views.single_document, name='document'),
    path('corpora', views.corpora, name='corpora'),
    path('corpus/<int:corpus_id>', views.corpus, name='corpus')
]
