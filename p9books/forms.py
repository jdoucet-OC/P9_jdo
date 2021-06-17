from django import forms
from django.forms import ModelForm, Textarea
from .models import Ticket, Review


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
        CHOICE = [('1', 1), ('2', 2), ('3', 3),
                  ('4', 4), ('5', 5)]
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
                choices=CHOICE
            )
        }

