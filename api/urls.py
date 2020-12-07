from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import api_basket, api_favorites, api_follow, UserViewSet, api_ingredients

API_VERSION = 'v1'

router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    # path(f'{API_VERSION}/api-token-auth/', obtain_auth_token),
    re_path(API_VERSION + r'/purchases/(?P<recipe_id>\d+)?$', api_basket),
    re_path(API_VERSION + r'/subscriptions/(?P<author_id>\d+)?$', api_follow),
    re_path(API_VERSION + r'/favorites/(?P<recipe_id>\d+)?$', api_favorites),
    re_path(API_VERSION + r'/ingredients/',
            api_ingredients), # ?query=${text}
    path(f'{API_VERSION}/', include(router.urls)),
]
