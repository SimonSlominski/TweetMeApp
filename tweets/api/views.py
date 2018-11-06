from rest_framework import generics
from rest_framework import permissions
from tweets.models import Tweet
from django.db.models import Q
from .pagination import StandardResultsSetPagination
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
    pagination_class = StandardResultsSetPagination

    def get_queryset(self, *args, **kwargs):
        """im_following is variable to show only tweets from user i am following"""
        im_following = self.request.user.profile.get_following()  # none
        qs1 = Tweet.objects.filter(user__in=im_following)
        qs2 = Tweet.objects.filter(user=self.request.user)
        """ Showing my tweets and tweets from user I am following"""
        qs = (qs1 | qs2).distinct().order_by("-timestamp")
        """The other way to sort tweets is to create class Meta: ordering = ['-timestamp'] in models.py + makemigrations/migrate"""
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

"""
class SearchAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all().order_by("-timestamp")
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query)
                    )
        return qs"""
