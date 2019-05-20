from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.article, name='article'),
    path('category/<str:category>/', views.search_category, name='category'),
    path('archive/<str:year_month>/', views.search_archive, name='archive'),
]