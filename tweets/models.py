from django.conf import settings
from django.urls import reverse_lazy
from django.db import models
from .validators import validate_content
from django.utils import timezone


class TweetManager(models.Manager):
    def retweet(self, user, parent_obj):
        """ Retweet the original tweet, not somebody else retweet of that tweet"""
        if parent_obj.parent:
            og_parent = parent_obj.parent
        else:
            og_parent = parent_obj

        qs = self.get_queryset().filter(
            user=user, parent=og_parent
        ).filter(
            timestamp__year=timezone.now().year,
            timestamp__month=timezone.now().month,
            timestamp__day=timezone.now().day,
        )
        if qs.exists():
            return None

        obj = self.model(
            parent=og_parent,
            user=user,
            content=parent_obj.content,
        )
        obj.save()

        return obj

    def like_toggle(self, user, tweet_obj):
        if user in tweet_obj.liked.all():
            is_liked = False
            tweet_obj.liked.remove(user)
        else:
            is_liked = True
            tweet_obj.liked.add(user)
        return is_liked


class Tweet(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL)
    content     = models.CharField(max_length=160, validators=[validate_content])
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    parent      = models.ForeignKey("self", blank=True, null=True) # Retweet
    liked       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply       = models.BooleanField(verbose_name='Is a reply?', default=False)

    objects = TweetManager()

    def __str__(self):
        return str(self.content)

    def get_absolute_url(self):
        return reverse_lazy("tweet:detail", kwargs={"pk":self.pk})

    class Meta:
        ordering = ['-timestamp']
