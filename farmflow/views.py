from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from .forms import RegisterForm, LoginForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from .forms import UpdateUserForm, UpdateProfileForm
from .models import *
from django.db.models import Count
# import jwt
# from django.conf import settings
# from django.http import HttpResponse



# Create your views here.
@login_required
def index(request):
    user = request.user
    if not user.is_authenticated:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    if farmer := user.farmer.first():
        farms = Farm.objects.filter(owner=user).prefetch_related('crops').all()
        crops = Crop.objects.filter(id__in=[crop.id for farm in farms for crop in farm.crops.all()]).distinct()
        production_stages = CropProductionStage.objects.filter(farm__in=farms).order_by('-planted_date')
        produce = Produce.objects.filter(farmer=user.profile)
        tags = Tag.objects.filter(produce__in=produce)
        farm_count = farms.count()
        crop_counts = [farm.crops.count() for farm in farms]
        total_crop_count = sum(crop_counts)
        value_chain_count = ValueChainChoice.objects.filter(farm__owner=request.user).distinct().count()
        produce_count = Produce.objects.filter(farmer=user.profile).count()

        
    else:
        # Show empty fields if user does not have a farmer object
        crops = Crop.objects.none()
        farms = Farm.objects.none()
        production_stages = CropProductionStage.objects.none()
        produce = Produce.objects.none()
        tags = Tag.objects.none()
        total_crop_count = 0
        
    context = {'crops': crops, 'farms': farms, 'production_stages': production_stages, 'produce': produce,'tags': tags,'farm_count': farm_count, 'crop_counts': crop_counts,'total_crop_count': total_crop_count,'value_chain_count': value_chain_count,'produce_count': produce_count,}
    return render(request, 'bootstrap/index.html', context)


def Static(request):
    return render(request, 'bootstrap/layout-static.html')

def LigthNav(request):
    return render(request, 'bootstrap/layout-sidenav-light.html')

def Chart(request):
    return render(request, 'bootstrap/charts.html')

def Table(request):
    user = request.user
    if not user.is_authenticated:
        # Redirect to login page if user is not authenticated
        return redirect('login')
    if farmer := user.farmer.first():
        farms = Farm.objects.filter(owner=user).prefetch_related('crops').all()
        production_stages = CropProductionStage.objects.filter(farm__in=farms).order_by('-planted_date')
        produce = Produce.objects.filter(farmer=user.profile)
        tags = Tag.objects.filter(produce__in=produce)
        
    else:
        # Show empty fields if user does not have a farmer object
        farms = Farm.objects.none()
        production_stages = CropProductionStage.objects.none()
        produce = Produce.objects.none()
        tags = Tag.objects.none()
    context = { 'farms': farms, 'production_stages': production_stages, 'produce': produce,'tags': tags}
    return render(request, 'bootstrap/tables.html', context)

def NotFound(request):
     return render(request, 'bootstrap/404.html')

def Unauthorised(request):
        return render(request, 'bootstrap/401.html')

def ServerError(request):
        return render(request, 'bootstrap/500.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})
    

# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    farms = Farm.my_farms(request.user.id)
    crop_counts = [farm.crops.count() for farm in farms]
    crop_count = sum(crop_counts)
    farm_count = farms.count()
    produce_count = Produce.objects.filter(farmer=profile).count()
    value_chain_count = ValueChainChoice.objects.filter(farm__owner=request.user).distinct().count()
    value_chains = ValueChainChoice.objects.filter(farm__owner=request.user).distinct()


    context = {
        'profile': profile,
        'crop_counts': crop_counts,
        'farm_count': farm_count,
        'produce_count': produce_count,
        'value_chain_count': value_chain_count,
        'crop_count': crop_count,
        'value_chains': value_chains,
    }
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})