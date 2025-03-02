from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from api.serializers import (
    BaksetSerializer, FavoriteSerializer,
    FollowSerializer, IngredientSerializer, UserSerializer, )
from recipes.models import Ingredient, Recipe


User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, ]

    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET', 'POST', 'DELETE'])
# @permission_classes([IsAuthenticated, ])
def api_basket(request, recipe_id=None):
    if request.user.is_authenticated:
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
            return Response({'success': True}, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            user = request.user
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            user.basket.remove(recipe)
            return Response({'success': True}, status=status.HTTP_200_OK)
    else:
        if request.method == 'GET':
            request.session['foo'] = 'bar'
            return Response({'session': request.session,
                             'foo': request.session['foo']})
        elif request.method == 'POST':
            recipe_id = request.data.get('recipe')
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            request.session.setdefault('basket', [])
            request.session.setdefault('basket_len', 0)
            request.session['basket'].append(recipe.id)
            request.session['basket_len'] = len(request.session['basket'])
            return Response({'success': True}, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, pk=recipe_id)
            request.session.setdefault('basket', [])
            request.session.setdefault('basket_len', 0)
            if recipe.id in request.session['basket']:
                request.session['basket'].remove(recipe.id)
                request.session['basket_len'] = len(request.session['basket'])
                return Response({'success': True}, status=status.HTTP_200_OK)
            else:
                return Response({'success': False},
                                status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def api_favorites(request, recipe_id=None):
    if request.method == 'GET':
        if recipe_id:
            user = request.user
            queryset = get_object_or_404(
                user.favorite_recipes, recipe__id=recipe_id)
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
        return Response({'success': True}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user.favorite_recipes.remove(recipe)
        return Response({'success': True}, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated, ])
def api_follow(request, author_id=None):
    if request.method == 'GET':
        if author_id:
            user = request.user
            queryset = get_object_or_404(
                user.favorite_authors, recipe__id=author_id)
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
        return Response({'success': True}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        user = request.user
        author = get_object_or_404(User, pk=author_id)
        user.favorite_authors.remove(author)
        return Response({'success': True}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def api_ingredients(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query and len(query) > 2:
            ingredients = Ingredient.objects.filter(name__icontains=query)
        elif query:
            return Response(
                {
                'success': False,
                'detail': 'too short query, need 3 symbol minimum',
                },
                exception=status.HTTP_400_BAD_REQUEST
            )
        else:
            ingredients = Ingredient.objects.all()
        serializer = IngredientSerializer(ingredients, many=True)
        return Response(serializer.data)
