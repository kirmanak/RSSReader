from datetime import datetime

from django.db import models
from django.utils.timezone import utc
from feedparser import parse


# Create your models here.
class Feed(models.Model):
    name = models.CharField(max_length=200, unique=True, blank=False, null=False)
    url = models.URLField(unique=True, blank=False, null=False)

    def fetch(self):
        feed_dict = parse(self.url)
        for entry in feed_dict['entries']:
            # if there are no posts with such a link
            if not Post.objects.filter(link=entry['link']).count():
                Post.objects.create(
                    title=entry['title'],
                    author=entry['author'],
                    feed=self,
                    description=entry['summary'],
                    link=entry['link'],
                    date=datetime(*entry.published_parsed[:6], tzinfo=utc)
                )

    def as_dist(self):
        return {
            "id": self.pk,
            "name": self.name,
            "url": self.url
        }

    def __str__(self) -> str:
        return format("Feed(%s:%s)" % (self.name, self.url))


class Post(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.CharField(max_length=200, blank=False, null=False)
    feed = models.ForeignKey('Feed', blank=False, null=False, on_delete=models.CASCADE)
    description = models.TextField(blank=False, null=False)
    link = models.URLField(unique=True, blank=False, null=False)
    date = models.DateTimeField(blank=False, null=False)

    def as_dist(self):
        return {
            "id": self.pk,
            "title": self.title,
            "author": self.author,
            "feed_id": self.feed.pk,
            "description": self.description,
            "link": self.link,
            "date": self.date,
        }

    def __str__(self) -> str:
        return format("Post(%s:%s)" % (self.title, self.link))
