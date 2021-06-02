from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import Review, Ticket, UserFollows
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import TicketForm, ReviewForm
from itertools import chain

def login(request):
    """"""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('flux')
        else:
            messages.info(request, "*verifiez votre mot de passe ou nom d'utilisateur")
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    """"""
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    """"""
    reviews = Review.objects.all()
    ticketids = [review.ticket.id for review in reviews]
    tickets = Ticket.objects.all().exclude(id__in=ticketids)
    # tickets and reviews, sorted by time created
    combined = sorted(chain(tickets, reviews),
                      key=lambda instance: instance.time_created,
                      reverse=True)
    return render(request, 'flux.html', context={'objects': combined})


@login_required(login_url='login')
def make_ticket(request):
    """"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = TicketForm()
    return render(request, "make_ticket.html", {'form': form})


@login_required(login_url='login')
def make_review(request):
    """"""
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = ReviewForm()
    return render(request, "make_review.html", {'form': form})
