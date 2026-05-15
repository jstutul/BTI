from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from accounts.decorators import role_required
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, SignUpForm,InstitutionForm,ProfileForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
import resend
User = get_user_model()
from dashboard.utils.email_utils import send_html_email
from dashboard.views import generate_unique_branch_code

def register_institution(request):
    form = InstitutionForm()
    if request.method == 'POST':
        form = InstitutionForm(request.POST)

        if form.is_valid():
            branch_code = generate_unique_branch_code()
            user = User.objects.create_user(
                username=branch_code,
                password=branch_code,
                is_staff=True,
                is_active=False
            )
            profile = user.profile

            # # 4. create institution safely
            institution = form.save(commit=False)
            institution.profile = profile
            institution.branch_code = branch_code
            institution.is_active=False
            institution.save()

            name = form.cleaned_data.get("name")
            director = form.cleaned_data.get("director")
            email = form.cleaned_data.get("email")

            html_content = render_to_string("emails/institution_created.html", {
                "director":director,
                "username": branch_code,
                "password": branch_code,
                "name": name,
            })

            send_html_email(
                subject="Institution Account Created",
                to_email=email,
                html_content=html_content,
            )

            messages.success(
                request,
                f"Institution created! Username: {branch_code}, Password: {branch_code}"
            )
            return redirect('accounts:login')
        else:
            messages.error(request, "Form validation failed!")
    return render(request,'accounts/institution.html',{'form':form})


class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        # ✅ Username field class
        form.fields['username'].widget.attrs.update({
            'class': 'form-control custom-username',
            'placeholder': 'Enter username'
        })

        # ✅ Password field class
        form.fields['password'].widget.attrs.update({
            'class': 'form-control custom-password',
            'placeholder': 'Enter password'
        })

        return form
    def dispatch(self, request, *args, **kwargs):
        # get type from URL
        self.login_type = request.GET.get('type', None)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.get_user()
        actual_role = user.profile.role

        if self.login_type:
            if actual_role != self.login_type:
                messages.error(self.request, f"You cannot login as {self.login_type}")
                return redirect(f"/accounts/login/?type={self.login_type}")

        return super().form_valid(form)

    def get_success_url(self):
        user = self.request.user
        role = user.profile.role

        if role == 'admin':
            return reverse('dashboard:admin_dashboard')
        elif role == 'institution':
            return reverse('dashboard:institution_dashboard')
        elif role == 'student':
            return reverse('dashboard:student_dashboard')
        else:
            return '/'





class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Account created successfully.')
        return response







@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    context = {
        'user': user,
        'profile': profile,
        'institution': getattr(profile, 'institution', None),
        'student': getattr(profile, 'student', None),
        'can_edit': profile.role in ['admin', 'institution']
    }

    if profile.role == 'institution':
        context['institution'] = getattr(profile, 'institution', None)

    elif profile.role == 'student':
        context['student'] = getattr(profile, 'student', None)


    return render(request, 'accounts/profile.html', context)

@login_required
def profile_edit(request):

    user = request.user
    profile = user.profile

    # ❌ BLOCK STUDENT
    if profile.role == 'student':
        messages.error(request, "You are not allowed to edit profile.")
        return redirect('dashboard:profile_view')

    profile_form = ProfileForm(
        request.POST or None,
        request.FILES or None,
        instance=profile
    )

    institution_form = None

    if profile.role == 'institution':
        institution = profile.institution
        institution_form = InstitutionForm(
            request.POST or None,
            instance=institution
        )

    # ✅ SAVE
    if profile_form.is_valid() and (not institution_form or institution_form.is_valid()):

        profile_form.save()

        if institution_form:
            institution_form.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('accounts:profile_view')

    return render(request, 'accounts/edit.html', {
        'profile_form': profile_form,
        'institution_form': institution_form,
        'profile': profile
    })




class ResendPasswordResetForm(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):

        # Render subject
        subject = render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())  # remove newlines

        if html_email_template_name:
            html_content = render_to_string(html_email_template_name, context)
        else:
            html_content = render_to_string(email_template_name, context)
        text_content = render_to_string(email_template_name, context)

        try:
            send_html_email(
                subject=subject,
                to_email=to_email,
                html_content=html_content,
            )

        except Exception as e:
            import logging
            logger = logging.getLogger('dashboard')
            logger.error(f"Password reset email failed: {e}")


class CustomPasswordResetView(PasswordResetView):
    form_class = ResendPasswordResetForm
    template_name = 'accounts/password_reset.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    email_template_name = 'accounts/password_reset_email.txt'
    html_email_template_name = 'accounts/password_reset_email.html'
    success_url = '/accounts/password-reset/done/'