from rest_framework import generics
from rest_framework import permissions
from tweets.models import Tweet
from django.db.models import Q
from .serializers import TweetModelSerializer


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    # Protects from adding a tweet after copying the link and opening a new window in private mode.
    # Without a previous login, the following message will appear: "detail": "Authentication credentials were not provided."
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer

    def get_queryset(self):
        gs = Tweet.objects.all().order_by("-timestamp")
        """The other way to sort tweets is to create class Meta: ordering = ['-timestamp'] in models.py + makemigrations/migrate"""
        query = self.request.GET.get("q", None)
        if query is not None:
            gs = gs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
                # user__username is accessing the value of "user" attribute of each Tweet instance
            )
        return gs