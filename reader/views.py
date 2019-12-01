from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .models import *


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    feed = Feed.objects.first()
    if feed:
        feed.fetch()
        posts = list(Post.objects.filter(feed=feed))
    else:
        posts = list()
    return render(request, "index.html", locals())
