from django.forms import ModelForm, Textarea

from recipes.models import Recipe, TagRecipe


class RecipeForm(ModelForm):
    prefix = 'Recipe'

    class Meta:
        model = Recipe
        fields = ('name', 'cooking_time', 'description','image')
        labels = {
            'group': 'Тематическая группа',
            'text': 'Ваша заметка',
            'image': 'Изображение',
        }
        help_texts = {
            'group': 'Ваш пост появиться в этой группе',
            'text:': 'Здесь вы можете излить свои мысли',
            'image': 'Иллюстрация добавит выразительности',
        }
        widgets = {
            'text': Textarea(attrs={
                'placeholder': 'Здесь вы можете излить свои мысли',
                'overflow': 'auto',
            }),
        }
        error_messages = {
            'image': {
                'images': 'нужна каринка',
                'invalid_extension': 'картинка нужна',
            },
            'text': {
                'required': 'без гениальных мыслей нельзя',
            }
        }


class TagRecipeForm(ModelForm):
    prefix = 'Tags'

    class Meta:
        model = TagRecipe
        fields = '__all__'
