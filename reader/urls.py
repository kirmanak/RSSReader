from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('update', views.update),
    path('feeds', views.feeds),
    path('feed_posts', views.feed_posts),
]
