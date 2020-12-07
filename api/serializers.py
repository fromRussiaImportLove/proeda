from rest_framework import serializers
from django.contrib.auth import get_user_model
from recipes.models import Basket, Favorite, Follow, Ingredient


User = get_user_model()


class BaksetSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Basket
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Favorite
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Follow
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='name')
    dimension = serializers.CharField(source='unit')

    class Meta:
        model = Ingredient
        fields = ('title', 'dimension')

