from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from .forms import TweetModelForm
from .mixins import FormUserNeededMixin
from .models import Tweet


class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = 'tweets/create_view.html'
    success_url = '/tweet/create'


# class TweetUpdateView(LoginRequiredMixin, UpdateView):
#     queryset = Tweet.object.all() # powinno wyciągać jeden element a nie wszystkie // spróbować get_object
#     form_class = TweetModelForm
#     template_name = 'tweets/update_view.html'
#     success_url = '/tweet/'


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

