from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from api.views import BasketViewSet

API_VERSION = 'v1'

router = DefaultRouter()
router.register('purchases', BasketViewSet)
#router.register('posts/(?P<post_id>\d)/comments', CommentViewSet, basename='comment')

urlpatterns = [
    # path(f'{API_VERSION}/api-token-auth/', obtain_auth_token),
    # path(f'{API_VERSION}/purchases', api_basket),
    path(f'{API_VERSION}/', include(router.urls)),
]
