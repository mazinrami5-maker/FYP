from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from django.shortcuts import render, get_object_or_404
from .models import Project, Column, Task
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.views.decorators.csrf import csrf_exempt

#views


def home(request):
    return render(request, 'board/home.html')

def about(request):
    return render(request, 'board/about.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('projecthub')
        else:
            messages.error(request, "Invalid username or password")
     
           
   
    return render(request, 'board/login.html')

def register(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not full_name or not email or not username or not password:
            messages.error(request, "All fields are required")
            return render(request, 'board/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return render(request, 'board/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = full_name
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('login') 

    return render(request, 'board/register.html')


def projecthub(request):
    return render(request, 'board/projecthub.html')


def profile(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('full_name')
        user.email = request.POST.get('email')
        user.username = request.POST.get('username')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully")

    return render(request, 'board/profile.html')

def logout_view(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect('home') 



@login_required
def create_project(request):
    print("USER:", request.user, "AUTH:", request.user.is_authenticated)

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user  
            project.save()
            default_columns = ["To Do", "In Progress", "For Review", "Done"]
            for i, name in enumerate(default_columns):
                Column.objects.create(project=project, name=name, order=i)

            return redirect('projecthub')
    else:
        form = ProjectForm()

    return render(request, 'board/projecthub.html', {'form': form})

def projecthub(request):
    projects = Project.objects.filter(owner=request.user)
    return render(request, 'board/projecthub.html', {
        'projects': projects
    })

@login_required
def kanban(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    columns = Column.objects.filter(project=project).order_by('order')
    if not Column.objects.filter(project=project).exists():
        default_columns = ["To Do", "In Progress", "For Review", "Done"]
        for i, name in enumerate(default_columns):
            Column.objects.create(project=project, name=name, order=i)
    
    columns = Column.objects.filter(project=project).order_by('order')
    

    for column in columns:
        column.tasks = Task.objects.filter(column=column)

    context = {
        'project': project,
        'columns': columns,
    }
    return render(request, 'board/kanban.html', context)


@csrf_exempt
def add_task(request, project_id):

    if request.method == "POST":
        data = json.loads(request.body)

        column = Column.objects.get(id=data["column_id"])

        task = Task.objects.create(
            column=column,
            name=data["name"],
            description="",
            deadline=None,
        )

        return JsonResponse({
            "id": task.id,
            "name": task.name,
        })



@csrf_exempt
def move_task(request, project_id):
    if request.method == "POST":
        data = json.loads(request.body)
        task_id = data.get("task_id")
        new_column_id = data.get("new_column_id")

       
        task = Task.objects.get(id=task_id)
        new_column = Column.objects.get(id=new_column_id)
        task.column = new_column
        task.save()
         



@require_POST
def delete_task(request, project_id):
    data = json.loads(request.body)
    task_id = data.get("task_id")

    try:
        task = Task.objects.get(id=task_id)
        task.delete()
        return JsonResponse({"success": True})

    except Task.DoesNotExist:
        return JsonResponse({"success": True})

        
@require_POST
def update_task_name(request, project_id):
    data = json.loads(request.body)
    task_id = data.get("task_id")
    name = data.get("name")
    task = Task.objects.get(id=task_id)
    task.name = name
    task.save()
    return JsonResponse({"success": True})


@login_required
def update_task_details(request, task_id):
    if request.method == "POST":
        data = json.loads(request.body)
        task = get_object_or_404(Task, id=task_id)
        task.description = data.get("description", "")
        task.deadline = data.get("deadline") or None
        task.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)





