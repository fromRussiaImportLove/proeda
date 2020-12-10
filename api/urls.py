from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from api.views import (
    BasketViewSet, UserViewSet, api_basket, api_favorites, api_follow,
    api_ingredients)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('basket', BasketViewSet, basename='basket')

urlpatterns = [
    re_path(r'v1/purchases/(?P<recipe_id>\d+)?$', api_basket),
    re_path(r'v1/subscriptions/(?P<author_id>\d+)?$', api_follow),
    re_path(r'v1/favorites/(?P<recipe_id>\d+)?$', api_favorites),
    re_path(r'v1/ingredients/', api_ingredients),
    path('v1/', include(router.urls)),
]
