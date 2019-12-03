from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from .models import *


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return JsonResponse({'error': "Method is not allowed"}, status=405)

    return render(request, "index.html")


def update(request: HttpRequest) -> HttpResponse:
    try:
        feed = get_feed(request)
    except Exception as e:
        body, code = e.args
        return JsonResponse(body, status=code)

    feed.fetch()
    return JsonResponse({'result': "Feed successfully updated"})


def feeds(request: HttpRequest) -> HttpResponse:
    if request.method != "GET":
        return JsonResponse({'error': "Method is not allowed"}, status=405)

    return JsonResponse({'feeds': [
        feed.as_dist() for feed in Feed.objects.all()
    ]})


def feed_posts(request: HttpRequest) -> HttpResponse:
    try:
        feed = get_feed(request)
    except Exception as e:
        body, code = e.args
        return JsonResponse(body, status=code)

    return JsonResponse({
        'posts': [post.as_dist() for post in Post.objects.filter(feed=feed)]
    })


def get_feed(request: HttpRequest) -> Feed:
    if request.method != "GET":
        raise Exception({'error': "Method is not allowed"}, 405)

    params = request.GET
    if 'feed_id' not in params:
        raise Exception({'error': "Parameter 'feed_id' was not found"}, 400)

    try:
        feed_id = int(params['feed_id'])
    except ValueError:
        raise Exception({'error': "Parameter 'feed_id' must be an integer"}, 400)

    try:
        feed = Feed.objects.get(pk=feed_id)
    except OverflowError:
        raise Exception({'error': "Parameter 'feed_id' is too big for an integer"}, 400)
    except Feed.DoesNotExist:
        raise Exception({'error': "Feed does not exist"}, 404)
    except Exception:
        raise Exception({'error': 'Unexpected server error'}, 500)

    return feed
