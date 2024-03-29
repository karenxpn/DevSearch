from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from .utils import search_project, paginate_projects


def projects(request):
    projects, search_query = search_project(request)
    custom_range, projects = paginate_projects(request, projects, 6)

    context = {
        'projects': projects,
        'search_query': search_query,
        'custom_range': custom_range,
    }
    return render(request, 'projects/projects.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    form = ReviewForm()
    context = {
        'project': project,
        'form': form
    }

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.get_vote_count
        messages.success(request, 'Your vote was successfully placed')
        return redirect('project', pk=project.id)
    return render(request, 'projects/single_project.html', context)


@login_required(login_url='login')
def create_project(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        new_tags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()

            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            form.save_m2m()
            return redirect('account')

    context = {'form': form}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def update_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        new_tags = request.POST.get('newtags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in new_tags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)

            return redirect('account')

    context = {
        'form': form,
        'project': project
    }
    return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def delete_project(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')

    context = {'object': project}
    return render(request, 'delete_object.html', context)
