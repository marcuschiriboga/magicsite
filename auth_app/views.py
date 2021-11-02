from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.views.generic import View
# Create your views here.


class LoginFormView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, "login_view.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))
