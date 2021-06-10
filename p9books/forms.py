from django.forms import ModelForm, Textarea
from .models import Ticket, Review


class TicketForm(ModelForm):
    """"""
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(ModelForm):
    """"""
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {'body': Textarea(attrs={'cols': 40, 'rows': 10})}

