from django.urls import path, re_path
from recipes import views

urlpatterns = [
    path('basket/', views.basket, name='basket'),
    path('basket/download', views.basket_download, name='basket_download'),
    path('favorites/', views.favorites, name='favorites'),
    path('<int:recipe_id>-<slug:the_slug>',
         views.RecipeDetailView.as_view(), name='recipe'),
    path('', views.index, name='index'),
]
