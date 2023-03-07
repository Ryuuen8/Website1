from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Todo, Day
from datetime import datetime
from django.contrib import messages
from django.db.models import Q
# Create your views here.


def Login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Home')
            else:
                messages.error(request, 'Invalid Username or Password')
        else:
            messages.error(request, 'Invalid Username or Password')
    else:
        form = AuthenticationForm()
    return render(request, 'Website/login_register.html', {'form': form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Home')

    else:
        form = UserCreationForm()
    return render(request, 'Website/register.html', {'form': form})


def Logout(request):
    logout(request)
    return redirect('Login')


@login_required(login_url='Login')
def Home(request):
    time = Day.objects.all()
    todos = Todo.objects.filter(user=request.user)
    tasks_count = todos.count()
    now = datetime.now()
    context = {'todos': todos, 'tasks_count': tasks_count,
               'current_date': now.date(), 'time': time}
    return render(request, 'Website/home.html', context)


@login_required(login_url='Login')
def Add_Task(request):
    if request.method == "POST":
        task = request.POST.get('task')
        due_date_str = request.POST.get('due_date')
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        day_pk = request.POST.get('day')
        day = Day.objects.get(pk=day_pk)
        completed = False
        todo = Todo.objects.create(user=request.user,
                                   task=task, due_date=due_date, completed=completed, day=day)
        return redirect('Home')

    days = Day.objects.all()
    context = {'days': days}
    return render(request, 'Website/add_task.html', context)


@login_required
def Remove_Task(request, task_id):
    task = get_object_or_404(Todo, id=task_id)
    task.delete()
    return redirect('Home')
