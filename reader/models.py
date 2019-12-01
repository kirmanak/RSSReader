from django.db import models


# Create your models here.
class Feed(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def as_dist(self):
        return {
            "id": self.pk,
            "name": self.name,
            "url": self.url
        }

    def __str__(self) -> str:
        return format("Feed(%s:%s)" % (self.name, self.url))


class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    feed = models.ForeignKey('Feed', on_delete=models.CASCADE)
    description = models.TextField()
    link = models.URLField()
    date = models.DateTimeField()

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
