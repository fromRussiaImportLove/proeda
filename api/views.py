from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from api.permissions import IsOwnerOrReadOnly
from api.serializers import BaksetSerializer
from recipes.models import Basket, Recipe


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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, ])
def api_basket(request):
    if request.method == 'GET':
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


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated,])
def api_basket_detail(request, recipe_id):
    if request.method == 'GET':
        user = request.user
        queryset = get_object_or_404(user.basket, recipe__id=recipe_id)
        serializer = BaksetSerializer(queryset)
        return Response(serializer.data)

    elif request.method == 'DELETE':
        user = request.user
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        user.basket.remove(recipe)
        return Response('ok', status=status.HTTP_200_OK)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([IsOwnerOrReadOnly, IsAuthenticated])
# def api_comments_detail(request, post_id, comment_id):
#     post = get_object_or_404(Post, id=post_id)
#     comment = get_object_or_404(post.comments, id=comment_id)
#
#     if request.user != comment.author:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#
#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT' or request.method == 'PATCH':
#         serializer = CommentSerializer(comment,
#                                        data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
