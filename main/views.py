from django.shortcuts import render

from main.models import Experience

from main.models import Skill


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