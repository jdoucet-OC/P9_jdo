from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', views.login, name="login"),
    path('', views.login, name="login"),
    path('flux', views.home, name="flux"),
    path('logout', views.logout, name="logout"),
    path('new-ticket', views.make_ticket, name="new-ticket"),
    path('new-review', views.make_review, name="new-review"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('posts', views.posts, name="posts"),
    re_path(r'answer/(?P<tiquetid>[^/]+)$', views.answer_ticket, name='answer')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

