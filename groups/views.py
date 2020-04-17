
from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import CreateView,DetailView,ListView,RedirectView
from django.shortcuts import get_object_or_404
from groups.models import Group,GroupMember
from django.db.utils import IntegrityError

class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ('name','description',)
    model = Group


class SingleGroup(DetailView):
    model = Group

class ListGroups(ListView):
    model = Group


class JoinGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        print("mmd")
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,("warning already aa member! |"))
        else:
            messages.success(self.request,'you are now a member |')
        return super().get(request,*args,**kwargs)





class LeaveGroup(LoginRequiredMixin,RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug')).get()
        except membership.DoesNotExist:
            messages.warning(self.request, ("sorry you are not in this group! |"))
        else:
            membership.delete()
            messages.success(self.request,"you have left thr group! |")
        return super().get(request,*args,**kwargs)