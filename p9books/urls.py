from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login', views.login, name="login"),
    path('', views.login, name="login"),
    path('flux', views.home, name="flux"),
    path('logout', views.logout, name="logout"),
    path('new-ticket', views.make_ticket, name="new-ticket"),
    path('new-review', views.make_review, name="new-review"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('posts', views.posts, name="posts"),
]
