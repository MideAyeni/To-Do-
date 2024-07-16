from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    if request.method == 'POST':
        task_title = request.POST.get('task_title', '')
        is_urgent = request.POST.get('urgent') == 'on'
        completed = request.POST.get('completed') == 'on'

        # Check if task_title is not empty before saving
        if task_title.strip():
            new_task = Task(title=task_title, urgent=is_urgent, completed=completed)
            new_task.save()

        elif 'clear_completed' in request.POST:  # Handle clearing completed tasks
            Task.objects.filter(completed=True).delete()

        elif 'delete_tasks' in request.POST:  # Handle deleting selected tasks
            task_ids = request.POST.getlist('task_ids')
            Task.objects.filter(id__in=task_ids).delete()

        return redirect('task_list')  # Always redirect after POST to avoid resubmission issues

    # Fetch all tasks for rendering
    tasks = Task.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})