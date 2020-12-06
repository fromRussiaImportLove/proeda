from django.urls import path, re_path
from recipes import views

urlpatterns = [
    path('basket/', views.basket, name='basket'),
    path('basket/download', views.basket_download, name='basket_download'),
    path('subscriptions/', views.subscriptions, name='subscriptions'),
    path('favorites/', views.favorites, name='favorites'),
    path('@<slug:author_username>', views.profile, name='profile'),
    path('<int:recipe_id>-<slug:the_slug>',
         views.RecipeDetailView.as_view(), name='recipe'),
    path('', views.index, name='index'),
]
