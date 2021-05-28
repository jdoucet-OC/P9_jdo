from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import Review, Ticket, UserFollows
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .forms import TicketForm, ReviewForm


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
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'flux.html', context={'tickets': tickets, 'reviews': reviews})


@login_required(login_url='login')
def make_ticket(request):
    """"""
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
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
    else:
        form = ReviewForm()
    return render(request, "make_review.html", {'form': form})
