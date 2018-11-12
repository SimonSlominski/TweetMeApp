from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin, UserOwnerMixin
from .models import Tweet
from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseRedirect

"""CRUD = Create, Retrieve, Update, Delete"""

class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            new_tweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect("/")
        return HttpResponseRedirect(tweet.get_absolute_url())


class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    # success_url = '/tweet/create' It's not necessary after create def get_absolute_url(self) in models.py


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    queryset = Tweet.objects.all()
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    # success_url = '/tweet/' It's not necessary after create def get_absolute_url(self) in models.py


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    success_url = reverse_lazy('tweet:list') # tweet = namespace, list = name from tweets app urls
    # template_name = 'tweet_confirm_delete.html' There's no need to put template_name if you use name from 'ErrorPage'


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()


class TweetListView(LoginRequiredMixin, ListView):

    def get_queryset(self, *args, **kwargs):
        gs = Tweet.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            gs = gs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query) # user__username is accessing the value of "user" attribute of each Tweet instance
                )
        return gs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(*args, **kwargs)
        context['create_form'] = TweetModelForm()
        context['create_url'] = reverse_lazy("tweet:create")
        return context

