from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from accounts.forms import UserLoginForm, UserRegistrationForm

User = get_user_model()

"""
Pre-coded Class-Based and Function-Based Views for login, logout, registration,
home (index) and user password reset operations.
- Home CBV: returns user to the sites home page
- logout FBV: logs out user and returns to login page
- PasswordResetRequest CBV: returns a blank reset form and sends a reset email
- LoginView CBV: logs in user and returns home page
- RegisterUser CBV: registers user credentials and returns login page
"""


#
# Home view included for testing.
# Is irrelevant and can be removed or replaced.
# Includes predecessor dependence from `accounts:urls` home url
#
class Home(generic.View, LoginRequiredMixin):
    template_name = 'accounts/index.html'

    def get(self, request):
        return render(request, self.template_name)


#
# User logout function
#
def logout_user(request):
    logout(request)

    return redirect('accounts:login')


#
# CBV gets and checks if email exists in the db
# Sends the user with the associated email a reset token
#
class PasswordResetRequest(generic.View):
    template_name = 'accounts/password-reset.html'
    email_template_name = 'accounts/reset.html'  # template containing reset token

    # Returns a blank password reset request form
    def get(self, request):
        form = PasswordResetForm()

        return render(request, self.template_name, {'form': form})

    # Verifies email and sends reset token to the entered address on success
    def post(self, request):
        form = PasswordResetForm(request.POST)
        current_site = get_current_site(request)  # Get the current sites protocol and domain name

        if form.is_valid():
            data = form.cleaned_data['email']

            # Check if email is associated with a user in the db
            associated_users = User.objects.filter(Q(email=data))

            if associated_users.exists():
                for user in associated_users:
                    subject = 'Password Reset Requested'
                    email_template_name = self.email_template_name
                    context = {
                        'email': user.email,
                        'domain': current_site,
                        'site_name': 'SimpleAuthentication',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, context)

                    # Send email to user address
                    try:
                        send_mail(
                            subject, email, settings.EMAIL_HOST_USER,
                            [user.email], fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')

                    # Redirect user to page notifying user of the sent mail
                    return redirect('accounts:password-reset-done')

            message = messages.add_message(
                request, messages.ERROR,
                'No such user associated with the email provided.'
            )
            return render(request, self.template_name, {'form': form, 'message': message})

        message = messages.add_message(
            request, messages.ERROR,
            'Error validating form.'
        )
        return render(request, self.template_name, {'form': form, 'message': message})


#
# CBV for user login
#
class LoginView(generic.View):
    template_name = 'accounts/login.html'

    # Returns a blank login form
    def get(self, request):
        form = UserLoginForm()

        return render(request, self.template_name, {'form': form})

    # Verifies email and password
    def post(self, request):
        form = UserLoginForm(request.POST)

        if form.is_valid:
            email = request.POST.get('email')
            password = request.POST.get('password')
            remember_me = request.POST.get('remember_me')
            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)

                if remember_me:
                    # Set expiry to 2 weeks
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)

                return render(request, 'accounts/index.html', {'user': user})

            else:
                message = 'Invalid Credentials!'

                return render(request, self.template_name, {'form': form, 'message': message})

        message = 'Error validating form'

        return render(request, self.template_name, {'form': form, 'message': message})


#
# CBV for user registration
#
class RegisterUser(generic.CreateView):
    template_name = 'accounts/register.html'

    # Returns a blank registration form
    def get(self, request, **kwargs):
        form = UserRegistrationForm()

        return render(request, self.template_name, {'form': form})

    # Validates credentials: email, username and password
    def post(self, request, **kwargs):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # Do not save data in db
            user = form.save(commit=False)
            msg = user.username + ' created successfully. Please login to continue.'
            messages.add_message(request, messages.SUCCESS, _(
                msg
            ))

            # Save data in db
            form.save(commit=True)

            # Redirect user to login page
            return redirect('accounts:login')

        message = messages.add_message(
            request, messages.ERROR, 'Failed to create account. Please contact your local administrator'
        )

        return render(request, self.template_name, {'form': form, 'message': message})
