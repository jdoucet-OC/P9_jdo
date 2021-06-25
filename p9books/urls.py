from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', views.login, name="login"),
    path('', views.login, name="login"),
    path('register', views.register, name="register"),
    path('flux', views.home, name="flux"),
    path('logout', views.logout, name="logout"),
    path('new-ticket', views.make_ticket, name="new-ticket"),
    path('new-review', views.make_review, name="new-review"),
    path('subscribe', views.subscribe, name="subscribe"),
    path('posts', views.posts, name="posts"),
    re_path(r'answer/(?P<tiquetid>[^/]+)$',
            views.answer_ticket, name='answer'),
    re_path(r'edit-ticket/(?P<tiquetid>[^/]+)$',
            views.edit_ticket, name='edit-ticket'),
    re_path(r'edit-review/(?P<reviewid>[^/]+)$',
            views.edit_review, name='edit-review'),
    re_path(r'delete-ticket/(?P<tiquetid>[^/]+)$',
            views.delete_ticket, name='delete-ticket'),
    re_path(r'delete-review/(?P<reviewid>[^/]+)$',
            views.delete_review, name='delete-review'),
    re_path(r'unsubscribe/(?P<followid>[^/]+)$',
            views.unsubscribe, name='unsubscribe'),
    re_path(r'new-subscribe/(?P<userid>[^/]+)$',
            views.new_subscribe, name='new-subscribe'),
    path('search-user/', views.UserSearchView.as_view(),
         name='search-user')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
