from django import forms
from django.forms import ModelForm
from .models import Ticket, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class TicketForm(ModelForm):
    """"""
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),

        }


class ReviewForm(ModelForm):
    """"""
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        CHOICE = [('0', 0), ('1', 1), ('2', 2),
                  ('3', 3), ('4', 4), ('5', 5)]
        widgets = {
            'headline': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'body': forms.Textarea(
                attrs={
                    'class': 'form-control'
                }
            ),
            'rating': forms.RadioSelect(
                choices=CHOICE,
                attrs={
                    'class': 'custom-li',
                    'id': 'testtt'
                }
            )
        }


class NewUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(NewUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].help_text = ''
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].help_text = ''
        self.fields['password1'].label = 'Mot de passe'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].help_text = ''
        self.fields['password2'].label = 'Confirmez mot de passe'

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
