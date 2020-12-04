from rest_framework import serializers

from recipes.models import Basket, Favorite, Follow


class BaksetSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Basket
        fields = '__all__'

