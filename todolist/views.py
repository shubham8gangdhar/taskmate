from django.core import paginator
from django.db.models import manager
from django.shortcuts import render,redirect
from django.http import HttpResponse
from todolist.models import Tasklist
from todolist.forms import Taskform
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'index.html')
@login_required
def todolist(request):
    if request.method == 'POST':
        form=Taskform(request.POST or None)
        if form.is_valid:
            instance=form.save(commit=False)
            instance.manager=request.user
            instance.save()
        messages.success(request,('New task added'))
        return redirect('todolist')
    else:    
        all_tasks=Tasklist.objects.filter(manager=request.user)
        paginator=Paginator(all_tasks,5)
        page=request.GET.get('pg')
        all_tasks=paginator.get_page(page)
        return render(request,'todolist.html',{'all_tasks':all_tasks})

def contact(request):
    return render(request,'contact.html')

def delete_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    if task.manager == request.user:
        task.delete()
    else:
        messages.error(request,'Access Restricted')
    return redirect('todolist')

def completed_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    if task.manager == request.user:
        task.done = True
        task.save()
    else:
        messages.error(request,'Access Restricted')
    return redirect('todolist')

def pending_task(request,task_id):
    task=Tasklist.objects.get(pk=task_id)
    task.done = False
    task.save()
    return redirect('todolist')

def edit_task(request,task_id):
    if request.method == 'POST':
        task=Tasklist.objects.get(pk=task_id)
        form =Taskform(request.POST or None,instance = task)
        if form.is_valid():
            form.save()

        messages.success(request,('tsk edited'))
        return redirect('todolist')
    else:    
        task_obj=Tasklist.objects.get(pk=task_id)
        return render(request,'edit.html',{'task_obj':task_obj})
