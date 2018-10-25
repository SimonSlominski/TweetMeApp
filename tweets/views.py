from django.shortcuts import render
from .models import Tweet
from django.views.generic import DetailView, ListView


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()

    # def get_object(self):
    #     return Tweet.objects.get(id=1)


class TweetListView(ListView):
    queryset = Tweet.objects.all()

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        return context





# CRUD:
    # Create
    # Retrieve
    # Update
    # Delete
    # List / Search

