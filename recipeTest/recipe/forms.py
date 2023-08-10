from django import forms
from .models import Comment, Recipe


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('name', 'text')


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image']
