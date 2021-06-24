from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from .models import Review, Ticket, UserFollows
from django.contrib.auth.decorators import login_required
from .forms import TicketForm, ReviewForm, NewUserForm
from itertools import chain
from django.http import Http404
from django.views.generic.list import ListView


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
            messages.info(request,
                          "*verifiez votre mot de passe ou nom d'utilisateur")
            return redirect('login')

    else:
        return render(request, 'login.html')


def logout(request):
    """"""
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("flux")
        messages.error(request, "Unsuccessful registration")
    form = NewUserForm
    return render(request=request, template_name="register.html",
                  context={"register_form": form})


@login_required(login_url='login')
def home(request):
    """"""
    user = request.user
    follows = UserFollows.objects.filter(user=user.id)
    user_list = [user]
    for users in follows:
        user_list.append(users.followed_user.id)
    reviews = Review.objects.all().filter(user__in=user_list)
    tickets = Ticket.objects.all().filter(user__in=user_list)
    myreviews = Review.objects.all().filter(user=user)
    # filter unanswered tickets
    mytickets = []
    for review in myreviews:
        mytickets.append(review.ticket)
    # tickets and reviews, sorted by time created
    combined = sorted(chain(tickets, reviews),
                      key=lambda instance: instance.time_created,
                      reverse=True)
    return render(request, 'flux.html',
                  context={'objects': combined, 'reviews': mytickets})


@login_required(login_url='login')
def make_ticket(request):
    """"""
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES or None)
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
        reviewform = ReviewForm(request.POST)
        ticketform = TicketForm(request.POST, request.FILES or None)
        if reviewform.is_valid() and ticketform.is_valid():
            review = reviewform.save(commit=False)
            ticket = ticketform.save(commit=False)
            review.user = request.user
            ticket.user = request.user
            ticket.save()
            review.ticket = ticket
            review.save()
            return redirect('flux')
    else:
        reviewform = ReviewForm()
        ticketform = TicketForm()
    return render(request, "make_review.html",
                  {'reviewform': reviewform, 'ticketform': ticketform})


@login_required(login_url='login')
def subscribe(request):
    """"""
    user = request.user
    follows = UserFollows.objects.filter(user=user.id)
    followed = UserFollows.objects.filter(followed_user=user.id)
    return render(request, "subscribe.html",
                  {"follows": follows, "followed": followed})


@login_required(login_url='login')
def posts(request):
    """"""
    user = request.user
    tickets = Ticket.objects.filter(user=user.id)
    reviews = Review.objects.filter(user=user.id)
    combined = sorted(chain(tickets, reviews),
                      key=lambda instance: instance.time_created,
                      reverse=True)
    return render(request, 'posts.html', context={'objects': combined})


@login_required(login_url='login')
def answer_ticket(request, **kwargs):
    """"""
    ticketid = int(kwargs['tiquetid'])
    ticket = Ticket.objects.get(id=ticketid)
    if request.method == 'POST':
        reviewform = ReviewForm(request.POST)
        if reviewform.is_valid():
            review = reviewform.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('flux')
    else:
        reviewform = ReviewForm()

    return render(request, "answer_ticket.html",
                  {'reviewform': reviewform, 'ticket': ticket})


@login_required(login_url='login')
def edit_ticket(request, **kwargs):
    """"""
    ticketid = int(kwargs['tiquetid'])
    ticket = Ticket.objects.get(id=ticketid)
    if ticket.user != request.user:
        raise Http404("You are not allowed to edit this Ticket")
    ticketform = TicketForm(request.POST or None, instance=ticket)
    if ticketform.is_valid():
        ticketform.save()
        return redirect('posts')
    return render(request, "edit_ticket.html", {'ticketform': ticketform})


@login_required(login_url='login')
def edit_review(request, **kwargs):
    """"""
    reviewid = int(kwargs['reviewid'])
    review = Review.objects.get(id=reviewid)
    if review.user != request.user:
        raise Http404("You are not allowed to edit this Review")
    ticket = review.ticket
    reviewform = ReviewForm(request.POST or None, instance=review)
    if reviewform.is_valid():
        reviewform.save()
        return redirect('posts')
    return render(request, "edit_review.html",
                  {'reviewform': reviewform, 'ticket': ticket})


@login_required(login_url='login')
def delete_ticket(request, **kwargs):
    """"""
    ticketid = int(kwargs['tiquetid'])
    ticket = Ticket.objects.get(id=ticketid)
    if ticket.user != request.user:
        raise Http404("You are not allowed to edit this Ticket")
    else:
        ticket.delete()
    return redirect('posts')


@login_required(login_url='login')
def delete_review(request, **kwargs):
    """"""
    reviewid = int(kwargs['reviewid'])
    review = Review.objects.get(id=reviewid)
    if review.user != request.user:
        raise Http404("You are not allowed to edit this Review")
    else:
        review.delete()
    return redirect('posts')


@login_required(login_url='login')
def unsubscribe(request, **kwargs):
    """"""
    followid = int(kwargs['followid'])
    follow = UserFollows.objects.get(id=followid)
    if follow.user != request.user:
        raise Http404("You are not allowed to edit this Review")
    else:
        follow.delete()
    return redirect('subscribe')


class UserSearchView(ListView):
    """"""
    model = User
    template_name = 'search_results.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        query = self.request.GET.get('username')
        return User.objects.filter(username__contains=query)
