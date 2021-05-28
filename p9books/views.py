from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from .models import Review, Ticket, UserFollows
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('flux')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'flux.html', context={'tickets': tickets, 'reviews': reviews})
