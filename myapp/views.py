from django.contrib.auth.models import User
from myapp.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
import random


def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get("page")
    objects = paginator.get_page(page)

    return objects


def index(request):
    questions = paginate(Question.objects.order_by("-date_joined"), request)
    popular_tags = Tag.objects.order_by("-rating")[:15]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(
        request, "index.html", {"questions": questions, "popular_tags": popular_tags, "best_members": best_members}
    )


def hot_questions(request):
    questions = paginate(Question.objects.order_by("-rating"), request)
    popular_tags = Tag.objects.order_by("-rating")[:15]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(
        request,
        "hot_questions.html",
        {"questions": questions, "popular_tags": popular_tags, "best_members": best_members},
    )


def tag(request, name):
    tag = get_object_or_404(Tag, name=name)
    questions = paginate(Question.objects.filter(tags__name=tag).order_by("-rating"), request)
    popular_tags = Tag.objects.order_by("-rating")[:15]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(
        request,
        "tag.html",
        {"tag": tag, "questions": questions, "popular_tags": popular_tags, "best_members": best_members},
    )


def answers_for_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    question_answers = paginate(Answer.objects.filter(question_id=pk).order_by("-rating"), request, 3)
    popular_tags = Tag.objects.order_by("-rating")[:10]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(
        request,
        "question.html",
        {
            "question": question,
            "answers": question_answers,
            "popular_tags": popular_tags,
            "best_members": best_members,
        },
    )


def login(request):
    popular_tags = Tag.objects.order_by("-rating")[:10]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(request, "login.html", {"popular_tags": popular_tags, "best_members": best_members})


def signup(request):
    popular_tags = Tag.objects.order_by("-rating")[:10]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(request, "signup.html", {"popular_tags": popular_tags, "best_members": best_members})


def new_question(request):
    popular_tags = Tag.objects.order_by("-rating")[:10]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(request, "new_question.html", {"popular_tags": popular_tags, "best_members": best_members})


def settings(request):
    popular_tags = Tag.objects.order_by("-rating")[:10]
    best_members = Profile.objects.order_by("-rating")[:10]

    return render(request, "settings.html", {"popular_tags": popular_tags, "best_members": best_members})
