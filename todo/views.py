from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.db.models import Q


# Create your views here.
def index(request):
    if request.method == 'POST':
        task = Task(
          title=request.POST['title'], subject=request.POST['subject'],
          due_at=make_aware(parse_datetime(request.POST['due_at'])),
          content=request.POST.get('content', '')
                    )
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.subject = request.POST['subject']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.content = request.POST.get('content', '')
        task.save()
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)


def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)


def search(request):
    query = request.GET.get('q')
    if query:
        tasks = Task.objects.filter(Q(title__icontains=query))
    else:
        tasks = Task.objects.all()

    context = {
        'tasks': tasks,
        'query': query
    }
    return render(request, 'todo/search.html', context)


def search_subject(request):
    query_s = request.GET.get('q_s')
    if query_s:
        tasks = Task.objects.filter(Q(subject__icontains=query_s))
    else:
        tasks = Task.objects.all()

    context = {
        'tasks': tasks,
        'query_s': query_s
    }
    return render(request, 'todo/search_subject.html', context)
