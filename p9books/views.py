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
    """
    :param request: request object
    :return: login view
    """
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
    """
    :param request: request object
    :return: allows logout
    """
    auth.logout(request)
    return redirect('login')


def register(request):
    """
    :param request: request object
    :return: register view
    """
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
    """
    :param request: request object
    :return: flux homepage, shows tickets and reviews
    from oneself and the followed users
    """
    user = request.user
    follows = UserFollows.objects.filter(user=user.id)
    user_list = [user]
    for users in follows:
        user_list.append(users.followed_user.id)
    reviews = Review.objects.all().filter(user__in=user_list)
    tickets = Ticket.objects.all().filter(user__in=user_list)

    # filter the tickets the user hasn't answered
    mytickets = []
    myreviews = Review.objects.all().filter(user=user)
    for review in myreviews:
        mytickets.append(review.ticket.id)
    othertickets = Ticket.objects.all().exclude(id__in=mytickets)

    # tickets and reviews, sorted by time created
    combined = sorted(chain(tickets, reviews),
                      key=lambda instance: instance.time_created,
                      reverse=True)
    return render(request, 'flux.html',
                  context={'objects': combined, 'other': othertickets})


@login_required(login_url='login')
def make_ticket(request):
    """
    :param request: request object
    :return: ticket creation view
    """
    if request.method == 'POST':
        form = TicketForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.image = form.cleaned_data['image']
            ticket.user = request.user
            ticket.save()
            return redirect('flux')
    else:
        form = TicketForm()
    return render(request, "make_ticket.html", {'form': form})


@login_required(login_url='login')
def make_review(request):
    """
    :param request: request object
    :return: review creation view
    """
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
    """
    :param request: request object
    :return: followers view, followed
    users and the followers
    """
    user = request.user
    follows = UserFollows.objects.filter(user=user.id)
    followed = UserFollows.objects.filter(followed_user=user.id)
    return render(request, "subscribe.html",
                  {"follows": follows, "followed": followed})


@login_required(login_url='login')
def posts(request):
    """
    :param request: request object
    :return: own post view ( tickets, reviews )
    """
    user = request.user
    tickets = Ticket.objects.filter(user=user.id)
    reviews = Review.objects.filter(user=user.id)
    combined = sorted(chain(tickets, reviews),
                      key=lambda instance: instance.time_created,
                      reverse=True)
    return render(request, 'posts.html', context={'objects': combined})


@login_required(login_url='login')
def answer_ticket(request, **kwargs):
    """
    :param request: request object
    :param kwargs: tiquetid : database id of the ticket
    the review responds to
    :return: review creation view, responding to a
    ticket
    """
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
    """
    :param request: request object
    :param kwargs: tiquetid : database id of the
    ticket being edited
    :return: ticket edition view
    """
    ticketid = int(kwargs['tiquetid'])
    ticket = Ticket.objects.get(id=ticketid)
    if ticket.user != request.user:
        raise Http404("You are not allowed to edit this Ticket")
    ticketform = TicketForm(request.POST or None,
                            request.FILES or None, instance=ticket)
    if ticketform.is_valid():
        ticket.image = ticketform.cleaned_data['image']
        ticketform.save()
        return redirect('posts')
    return render(request, "edit_ticket.html", {'ticketform': ticketform})


@login_required(login_url='login')
def edit_review(request, **kwargs):
    """
    :param request: request object
    :param kwargs: reviewid : database id of the
    review being edited
    :return: review edition view
    """
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
    """
    :param request: request object
    :param kwargs: tiquetid : database id of the ticket
    being deleted
    :return: ticket deletion view
    """
    ticketid = int(kwargs['tiquetid'])
    ticket = Ticket.objects.get(id=ticketid)
    if ticket.user != request.user:
        raise Http404("You are not allowed to edit this Ticket")
    else:
        ticket.delete()
    return redirect('posts')


@login_required(login_url='login')
def delete_review(request, **kwargs):
    """
    :param request: request object
    :param kwargs: reviewid : database id of the review
    being deleted
    :return: review deletion view
    """
    reviewid = int(kwargs['reviewid'])
    review = Review.objects.get(id=reviewid)
    if review.user != request.user:
        raise Http404("You are not allowed to edit this Review")
    else:
        review.delete()
    return redirect('posts')


@login_required(login_url='login')
def unsubscribe(request, **kwargs):
    """
    :param request: request object
    :param kwargs: followid : database id of the
    userfollow object being deleted
    :return: userfollow deletion view
    """
    followid = int(kwargs['followid'])
    follow = UserFollows.objects.get(id=followid)
    if follow.user != request.user:
        raise Http404("You are not allowed to edit this Review")
    else:
        follow.delete()
    return redirect('subscribe')


@login_required(login_url='login')
def new_subscribe(request, **kwargs):
    """
    :param request: request object
    :param kwargs: userid : database id of the
    user being followed_user in userfollow model
    :return: new userfollow object
    """
    userid = int(kwargs['userid'])
    followeduser = User.objects.get(id=userid)
    newfollow = UserFollows(user=request.user, followed_user=followeduser)
    newfollow.save()
    return redirect('subscribe')


class UserSearchView(ListView):
    """
    model : User
        django User object
    template_name : str
        template used for search bar
    context_object_name : str
        context variable used (template)
    """
    model = User
    template_name = 'search_results.html'
    context_object_name = 'all_search_results'

    def get_queryset(self):
        """
        :return: user search bar, excluding already
        followed user and current user
        """
        query = self.request.GET.get('username')
        userid = self.request.user.id
        follows = UserFollows.objects.filter(user=userid)
        idlist = [userid]
        for follow in follows:
            idlist.append(follow.followed_user.id)
        query = User.objects.filter(username__contains=query)
        return query.exclude(id__in=idlist)
