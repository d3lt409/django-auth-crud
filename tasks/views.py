from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import TaskForm
from .models import Task
# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})

    body = request.POST
    if body["password1"] == body["password2"]:
        try:
            user = User.objects.create_user(
                username=body["username"], password=body["password1"])
            user.save()
            login(request, user)
            return redirect('tasks')
        except IntegrityError:
            return render(request, 'signup.html',
                          {'form': UserCreationForm, 'error': "User already exist"})
    return render(request, 'signup.html',
                  {'form': UserCreationForm, 'error': "Password do not match"})

@login_required
def tasks(request: WSGIRequest):
    return render(request, 'tasks.html', {
        'tasks': Task.objects.filter(user=request.user, complete_at__isnull=True).all()
    })

@login_required
def complete_task(request: WSGIRequest):
    return render(request, 'tasks.html', {
        'tasks': Task.objects.filter(user=request.user,complete_at__isnull=False).all()
    })

@login_required
def create_task(request: WSGIRequest):
    if request.method == "GET":
        return render(request, 'create_task.html',
                      {'form': TaskForm})
    try:
        body = request.POST
        task = Task.objects.create(
            title=body["title"], description=body["description"], user=request.user)

        task.save()
        return redirect('tasks')
    except Exception as e:
        return render(request, 'create_task.html',
                      {'form': TaskForm, 'error':e})

@login_required
def task_detail(request:WSGIRequest, id:int):
    task = get_object_or_404(Task, pk=id, user = request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task':task, "form":form
        })
    form = TaskForm(request.POST,instance=task )
    form.save()
    return redirect('tasks')

@login_required
def task_complete(request:WSGIRequest, id:int):
    task = get_object_or_404(Task, pk=id, user = request.user)
    task.complete_at = timezone.now()
    task.save()
    return redirect('tasks')

@login_required   
def task_delete(request:WSGIRequest,id:int):
    task = get_object_or_404(Task, pk=id, user = request.user)
    task.delete()
    return redirect('tasks')

@login_required
def signout(request: WSGIRequest):
    logout(request)
    return redirect('home')


def signin(request: WSGIRequest):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    body = request.POST
    user = authenticate(
        request, username=body["username"], password=body["password"])
    if not user:
        return render(request, 'signin.html', {
            'form': AuthenticationForm, "error": "Username and Password do not match"
        })
    login(request, user)
    return redirect('tasks')
