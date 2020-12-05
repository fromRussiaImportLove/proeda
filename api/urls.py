from django.urls import include, path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import api_basket, api_basket_detail

API_VERSION = 'v1'

router = DefaultRouter()
# router.register('purchases', BasketViewSet)
# router.register('posts/(?P<post_id>\d)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    # path(f'{API_VERSION}/api-token-auth/', obtain_auth_token),
    re_path(API_VERSION + r'/purchases/(?P<recipe_id>\d+)$', api_basket_detail),
    path(f'{API_VERSION}/purchases/', api_basket),
    path(f'{API_VERSION}/', include(router.urls)),
]
