from django.forms import ModelForm

from recipes.models import Recipe


class RecipeForm(ModelForm):
    prefix = 'Recipe'

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'description', 'image')

        error_messages = {
            'image': {
                'images': 'нужна каринка',
                'invalid_extension': 'картинка нужна',
            },
            'description': {
                'required': 'без гениальных мыслей нельзя',
            }
        }
