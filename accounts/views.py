from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .forms import SignupForm, EditProfileForm
from .models import User


class UserLoginView(LoginView):
    """ This view authenticates and validates user credentials provided in the login form. """
    template_name = 'accounts/login.html'


class SignupView(View):
    """ This view help a user to create an account. """
    
    form_class = SignupForm
    template_name = 'accounts/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()

        context = {'SignupForm': form}
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Account created successfully!')
            return redirect('login')

        context = {'SignupForm': form}
        return render(request, self.template_name, context)


@method_decorator(login_required(login_url='login'), name='get')
@method_decorator(user_passes_test(lambda user: user.is_staff is False and user.is_superuser is False), name='get')
class UserProfileView(View):
    """ This view allows a user to update his/her profile. """

    form_class = EditProfileForm
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        form_class = self.form_class(instance=request.user)
        password_change_form = PasswordChangeForm(request.user)

        context = {
            'EditProfileForm': form_class,
            'ChangePasswordForm': password_change_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form_class = self.form_class(request.POST, request.FILES, instance=request.user)
        password_change_form = PasswordChangeForm(user=request.user, data=request.POST)

        if form_class.is_valid():
            form_class.save()

            messages.info(request, 'User profile updated successfully!')
            return redirect('user_profile')
        
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_profile')
        
        else:
            if password_change_form.error_messages["password_mismatch"] or password_change_form.error_messages["password_incorrect"]:
                messages.error(request, f'{password_change_form.error_messages["password_mismatch"]}')
                messages.error(request, f'{password_change_form.error_messages["password_incorrect"]}')
            
            messages.error(request, f'{password_change_form.errors}')
        
        context = {
            'EditProfileForm': form_class,
            'ChangePasswordForm': password_change_form,
        }
        return render(request, self.template_name, context)


class LogoutUserView(LogoutView):
    """ This view logs out a user from the website. """
    template_name = 'accounts/login.html'
