import random
from django.shortcuts import reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from requests import request
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganiserAndLoginRequiredMixin
from django.core.mail import send_mail


class AgentListView(OrganiserAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agent_list.html'
    
    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentCreateView(OrganiserAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organiser = False
        user.set_password(f"{random.randint(0, 10000)}")
        user.save()
        Agent.objects.create(
            user=user,
            organisation=self.request.user.userprofile,
        )
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on ##.",
            from_email="admin@test.com",
            recipient_list=[user.email],
        )
        return super(AgentCreateView, self).form_valid(form)
        # agent.organisation = self.request.user.userprofile
        # agent.save()



class AgentDetailView(OrganiserAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentDeleteView(OrganiserAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    # queryset = Agent.objects.all()

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)


class AgentUpdateView(OrganiserAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    # queryset = Agent.objects.all()
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-update")

    def get_queryset(self):
        request_user_organisation = self.request.user.userprofile
        return Agent.objects.filter(organisation=request_user_organisation)