from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Notice
from .forms import RegisterForm, NoticeForm

def homepage(request):
    return redirect('login')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            if role == "Administrator":
                if user.is_superuser:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'login.html', {'error': 'Only Superuser can access Administrator role.'})
            elif role == "Senior Doctor":
                if user.groups.filter(name='Senior Doctors').exists():
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'login.html', {'error': 'You do not have Senior Doctor access.'})
            elif role == "Doctor":
                if user.groups.filter(name='Doctors').exists():
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'login.html', {'error': 'You do not have Doctor access.'})
            elif role == "Nurse":
                if user.groups.filter(name='Nurses').exists():
                    login(request, user)
                    return redirect('dashboard')
                else:
                    return render(request, 'login.html', {'error': 'You do not have Nurse access.'})
            else:
                return render(request, 'login.html', {'error': 'Invalid role selected.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    return render(request, 'login.html')


@login_required
def dashboard_view(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'notices': notices})

@login_required
@user_passes_test(lambda u: u.is_staff)
def post_notice_view(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()
            return redirect('dashboard')
    else:
        form = NoticeForm()
    return render(request, 'post_notice.html', {'form': form})

@login_required
def register_view(request):
    if not request.user.is_superuser:
        return render(request, 'logical_error.html', {'message': 'You do not have permission to create new users.'})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff)
def edit_notice_view(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = NoticeForm(instance=notice)
    return render(request, 'edit_notice.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def delete_notice_view(request, notice_id):
    notice = Notice.objects.get(id=notice_id)
    if request.method == 'POST':
        notice.delete()
        return redirect('dashboard')
    return render(request, 'delete_notice.html', {'notice': notice})
