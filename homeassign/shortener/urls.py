from django.urls import path

from . import views

urlpatterns = [
    path('s/<generated_redirect>/', views.redirects, name='redirects'),
    path('create/', views.create, name='create'),
]