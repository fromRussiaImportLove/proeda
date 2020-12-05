from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from api.permissions import IsOwnerOrReadOnly
from api.serializers import *
from recipes.models import Recipe, User


# class BasketViewSet(viewsets.ModelViewSet):
#     # permission_classes = [IsAuthenticated]
#
#     queryset = Basket.objects.all()
#     serializer_class = BaksetSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class CommentViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsOwnerOrReadOnly, IsAuthenticated]
#     serializer_class = CommentSerializer
#
#     def get_queryset(self):
#         post = get_object_or_404(Post, id=self.kwargs['post_id'])
#         return post.comments.all()
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def api_basket(request, recipe_id=None):
    if request.method == 'GET':
        if recipe_id:
            user = request.user
            queryset = get_object_or_404(user.basket, recipe__id=recipe_id)
            serializer = BaksetSerializer(queryset)
            return Response(serializer.data)

        user = request.user
        recipes = user.basket.all()
        serializer = BaksetSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        recipe_id = request.data.get('recipe')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user.basket.append(recipe)
        return Response('ok', status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user.basket.remove(recipe)
        return Response('ok', status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def api_favorites(request, recipe_id=None):
    if request.method == 'GET':
        if recipe_id:
            user = request.user
            queryset = get_object_or_404(user.favorite_recipes, recipe__id=recipe_id)
            serializer = FavoriteSerializer(queryset)
            return Response(serializer.data)

        user = request.user
        recipes = user.favorite_recipes.all()
        serializer = FavoriteSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        recipe_id = request.data.get('recipe')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user.favorite_recipes.append(recipe)
        return Response('ok', status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user.favorite_recipes.remove(recipe)
        return Response('ok', status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def api_follow(request, author_id=None):
    if request.method == 'GET':
        if author_id:
            user = request.user
            queryset = get_object_or_404(user.favorite_authors, recipe__id=author_id)
            serializer = FollowSerializer(queryset)
            return Response(serializer.data)

        user = request.user
        recipes = user.favorite_authors.all()
        serializer = FollowSerializer(recipes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = request.user
        author_id = request.data.get('author_id')
        author = get_object_or_404(User, pk=author_id)
        user.favorite_authors.append(author)
        return Response('ok', status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user = request.user
        author = get_object_or_404(User, pk=author_id)
        user.favorite_authors.remove(author)
        return Response('ok', status=status.HTTP_200_OK)
