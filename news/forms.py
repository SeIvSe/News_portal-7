from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class CreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get("author")
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title is None or len(title) < 4:
            raise ValidationError({
                    "title": "Название не может быть менее 4 символов или пустым."
            })

        return cleaned_data


class SearchForm(forms.ModelForm):
   class Meta:
       model = Post
       fields =  '__all__'

class DeleteForm(forms.ModelForm):
   class Meta:
       model = Post
       fields =  '__all__'