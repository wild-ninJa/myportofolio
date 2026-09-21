from main.models import Experience, Skill, Project
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from main.forms import ProjectForm, ExperienceForm


def show_main(request):
    context = {
        "name": "Husainah Syamsiah",
        "npm": "2506589036",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "2nd year CS student at Universitas Indonesia. Would appreciate "
            "you for giving her a free but fresh Pizza. Lorem Ipsum Lorem "
            "Lorem Lorem Ipsum Yayaya filler filler filler filler fiilllerrrr. Happy Ending. Amiin."
        ),
    }
    return render(request, "index.html", context)

# Experience area

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "New Experience added!")
        return redirect("main:show_experience")

    context = {
        "name": "Husainah Syamsiah",
        "form": form,
    }
    return render(request, "experience_form.html", context)

def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experiences = [experience.object for experience in experiences]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Husainah Syamsiah",
        "experience_list": experiences,
        "title_query": title_query,
    }
    return render(request, "experience.html", context) # TODO: MAKE EXPERIENCE.HTML

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience deleted!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")

# Skill area

def show_skill(request):
    context = {
        "name": "Husainah Syamsiah",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)

# Projects area

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Husainah Syamsiah",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Burhan",
        "project_list": projects,
        "title_query": title_query,
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")