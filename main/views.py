from main.models import Experience, Skill
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render


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


def show_experience(request):
    context = {
        "name": "Husainah Syamsiah",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_skill(request):
    context = {
        "name": "Husainah Syamsiah",
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skill.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Burhan",
        "form": form,
    }
    return render(request, "projects_form.html", context)