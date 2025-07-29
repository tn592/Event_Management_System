from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.db.models import Prefetch
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, TemplateView, UpdateView
from django.views import View
from django.views.generic.base import ContextMixin
from users.forms import CreateGroupForm, CustomPasswordChangeForm, CustomPasswordResetConfirmForm, CustomPasswordResetForm, CustomRegistrationForm
from django.contrib import messages
from users.forms import LoginForm, AssignRoleForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import user_passes_test
from users.forms import EditProfileForm
from django.contrib.auth import get_user_model


User = get_user_model()


class EditProfileView(UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'accounts/update_profile.html'
    context_object_name = 'form'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.save()
        return redirect('profile')


def is_admin(user):
    return user.groups.filter(name='Admin').exists()


def sign_up(request):
    if request.method == "POST":
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            print("user", user)
            user.set_password(form.cleaned_data.get("password"))
            print(form.cleaned_data)
            user.is_active = False
            user.save()
            messages.success(
                request, "A confirmation mail sent. Please check your email"
            )
            return redirect("sign_in")
        else:
            print("Form is not valid")
    else:
        form = CustomRegistrationForm()

    return render(request, "registration/register.html", {"form": form})


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        return next_url if next_url else super().get_success_url()


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("sign_in")
        else:
            return HttpResponse("Invalid Id or token")
    except User.DoesNotExist:
        return HttpResponse("User not Found")


@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name 
        else:
            user.group_name = "No Group Assigned"
    return render(request, 'admin/admin_dashboard.html', {'users':users})


is_admin_decorator = user_passes_test(is_admin, login_url='no_permission')


@method_decorator(is_admin_decorator, name='dispatch')
class AssignRole(ContextMixin, View):
    login_url = 'sign_in'
    template_name = 'admin/assign_role.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', AssignRoleForm)
        return context 

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = AssignRoleForm(request.POST)
        user_id = kwargs.get('user_id')
        user = User.objects.get(id=user_id)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Remove old data
            user.groups.add(role)
            messages.success(request, f'User {user.username} has been assigned to the {role.name} role')
            context = self.get_context_data(form=form)
            return render(request, self.template_name, context)


is_admin_decorator = user_passes_test(is_admin, login_url='no_permission')


@method_decorator(is_admin_decorator, name='dispatch')
class CreateGroup(ContextMixin, View):
    login_url = 'sign_in'
    template_name = 'admin/create_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = kwargs.get('form', CreateGroupForm)
        return context 

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, "Group Created Successfully")
            context = self.get_context_data(form=form)
            return render(request, self.template_name, context)


is_admin_decorator = user_passes_test(is_admin, login_url='no_permission')


@method_decorator(is_admin_decorator, name='dispatch')
class GroupList(ListView):
    template_name = 'admin/group_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        return Group.objects.prefetch_related('permissions').all()


@user_passes_test(is_admin, login_url='no_permission')
def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
        messages.success(request, f"Group '{group.name}' has been deleted successfully.")
    except Group.DoesNotExist:
        return HttpResponse("Group not Found")
    return redirect('group_list')

class ChangePassword(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = CustomPasswordChangeForm


class ProfileView(TemplateView):
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['username'] = user.username
        context['email'] = user.email 
        context['name'] = user.get_full_name()
        context['phone'] = user.phone
        context['profile_image'] = user.profile_image
        context['member_since'] = user.date_joined
        context['last_login'] = user.last_login
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign_in')
    html_email_template_name = 'registration/reset_email.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context

    def form_valid(self, form):
        messages.success(self.request, 'A Reset email sent. Please check your email')
        return super().form_valid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordResetConfirmForm
    template_name = 'registration/reset_password.html'
    success_url = reverse_lazy('sign_in')

    def form_valid(self, form):
        messages.success(self.request, 'Password Reset Successfully')
        return super().form_valid(form)
