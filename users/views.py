from asyncio import Event
from django.contrib.auth import login, logout
from django.db.models import Prefetch
from django.shortcuts import HttpResponse, redirect, render
from django.contrib.auth.models import User, Group
from users.forms import CreateGroupForm, CustomRegistrationForm
from django.contrib import messages
from users.forms import LoginForm, AssignRoleForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test


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


def sign_in(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("home")
    return render(request, "registration/login.html", {"form": form})


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


@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == "POST":
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear() # Remove old data
            user.groups.add(role)
            messages.success(request, f'User {user.username} has been assigned to the {role.name} role')
            return redirect('admin_dashboard')
    return render(request, 'admin/assign_role.html', {'form':form})


@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    
    if request.method == "POST":
        form = CreateGroupForm(request.POST)

        if form.is_valid():
            group = form.save()
            messages.success(request, f'Group {group.name} has been created successfully')
            return redirect('create_group')

    return render(request, 'admin/create_group.html', {'form': form})


@user_passes_test(is_admin, login_url='no_permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {'groups':groups})


@user_passes_test(is_admin, login_url='no_permission')
def delete_group(request, group_id):
    try:
        group = Group.objects.get(id=group_id)
        group.delete()
        messages.success(request, f"Group '{group.name}' has been deleted successfully.")
    except Group.DoesNotExist:
        return HttpResponse("Group not Found")
    return redirect('group_list')


