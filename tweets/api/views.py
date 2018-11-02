from rest_framework import generics
from tweets.models import Tweet
from django.db.models import Q
from .serializers import TweetModelSerializer


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        gs = Tweet.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            gs = gs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
                # user__username is accessing the value of "user" attribute of each Tweet instance
            )
        return gs