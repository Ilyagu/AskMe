from django.contrib.auth.models import User
from myapp.models import Profile, Question, Answer, Tag, LikeQuestion, LikeAnswer
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render
import random


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get("page")
    objects = paginator.get_page(page)

    return objects


def index(request):
    questions = paginate(Question.objects.new_questions(), request)
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()

    return render(
        request, "index.html", {"questions": questions, "popular_tags": popular_tags, "best_members": best_members}
    )


def hot_questions(request):
    questions = paginate(Question.objects.hot_questions(), request)
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()

    return render(
        request,
        "hot_questions.html",
        {"questions": questions, "popular_tags": popular_tags, "best_members": best_members},
    )


def tag(request, name):
    try:
        tag = Tag.objects.get(name=name)
        questions = paginate(Question.objects.by_tag(name), request)
        popular_tags = Tag.objects.popular_tags()
        best_members = Profile.objects.best_members()

        return render(
            request,
            "tag.html",
            {"tag": tag, "questions": questions, "popular_tags": popular_tags, "best_members": best_members},
        )
    except Tag.DoesNotExist:
        raise Http404


def answers_for_question(request, pk):
    try:
        question = Question.objects.get(pk=pk)
        question_answers = paginate(Answer.objects.by_question(pk), request, 3)
        popular_tags = Tag.objects.popular_tags()
        best_members = Profile.objects.best_members()

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
    except Question.DoesNotExist:
        raise Http404


def login(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()

    return render(request, "login.html", {"popular_tags": popular_tags, "best_members": best_members})


def signup(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()

    return render(request, "signup.html", {"popular_tags": popular_tags, "best_members": best_members})


def ask(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()

    return render(request, "new_question.html", {"popular_tags": popular_tags, "best_members": best_members})


def settings(request):
    popular_tags = Tag.objects.popular_tags()
    best_members = Profile.objects.best_members()

    return render(request, "settings.html", {"popular_tags": popular_tags, "best_members": best_members})
