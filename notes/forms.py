from django import forms
from .models import Note, Comment, NoteImage
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class NoteForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'class': 'form-control',
            'accept': 'image/*'
        }),
        label='Zdjęcia'
    )

    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'is_published']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 5,
                'class': 'form-control',
                'placeholder': 'Wpisz treść notatki'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Wybierz kategorię'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Wpisz tytuł notatki'
            }),
        }
        labels = {
            'title': 'Tytuł',
            'content': 'Treść',
            'category': 'Przedmiot',
            'is_published': 'Opublikuj notatkę'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Napisz komentarz...',
                'class': 'form-control'
            })
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
            'username': 'Nazwa użytkownika',
            'email': 'Email',
            'password1': 'Hasło',
            'password2': 'Potwierdź hasło',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

from django import forms
from django.contrib.auth.models import User

class UsernameChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {'username': 'Nowa nazwa użytkownika'}