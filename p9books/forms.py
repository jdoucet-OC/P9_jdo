from django.forms import ModelForm
from .models import Ticket, Review


class TicketForm(ModelForm):
    """"""
    class Meta:
        model = Ticket
        fields = ['title', 'description']


class ReviewForm(ModelForm):
    """"""
    class Meta:
        model = Review
        title = None
        description = None
        image = None
        fields = ['rating', 'headline', 'body']