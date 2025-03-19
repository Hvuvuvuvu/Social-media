from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from my.forms import CommentForm, PubForm
from my.mixins import UserIsOwnerMixin
from my.models import Publication, Comment


@login_required
def user_pub(request):
    pubs = Publication.objects.filter(creator=request.user).order_by('-publicate_date')
    return render(request, 'user_pub.html', {'pubs': pubs})

class PubList(ListView):
    model = Publication
    template_name = 'pub_list.html'
    context_object_name = 'pubs'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get("status", "")
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class PubDetailView(DetailView):
    model = Publication
    template_name = 'pub_detail.html'
    context_object_name = 'pub'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['comment_form'] = CommentForm()
        return context


class PubCreateView(CreateView):
    model = Publication
    template_name = "pub_form.html"
    form_class = PubForm
    success_url = reverse_lazy("pub_list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class PubDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = Publication
    template_name = "pub_confirm_delete.html"
    success_url = reverse_lazy('pub_list')


class PubEditView(UpdateView):
    model = Publication
    template_name = "pub_form.html"
    form_class = PubForm
    success_url = reverse_lazy('pub_list')


class PubPublishView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def post(self, request, *args, **kwargs):
        publication = self.get_object()
        publication.status = "PU"
        publication.save()
        return HttpResponseRedirect(reverse_lazy("pub_list"))

    def get_object(self):
        pub_id = self.kwargs.get("pk")
        return get_object_or_404(Publication, pk=pub_id)


class CustomLoginView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "login"


class RegisterView(CreateView):
    template_name = "register.html"
    form_class = UserCreationForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse_lazy("login"))


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'pub_detail.html'
    context_object_name = 'pub'

    def form_valid(self, form):
        pub = get_object_or_404(Publication, pk=self.kwargs['pk'])
        form.instance.pub = pub
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('pub_detail', kwargs={'pk': self.kwargs['pk']})