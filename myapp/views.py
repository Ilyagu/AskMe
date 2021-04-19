from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import render
import random

questions = [
    {
        'id': i,
        'title': f'Title #{i}',
        'text': f'Question\'s text #{i}',
        'likes': random.randint(0, 50),
        'dislikes': random.randint(0, 50),
        'number_of_answers': 2,
        'tags_name': {f'Tag{random.randint(0, 9)}', f'Tag{random.randint(0, 9)}'}
    } for i in range(30)
]

answers = [
    {
        'id': i,
        'question_id': i // 2,
        'text': f'Answer\'s text #{i}',
        'likes': i + 42,
        'dislikes': i + 24
    } for i in range(60)
]

tags = [
    {
        'id': i,
        'questions_id': {random.randint(0, 30), random.randint(0, 30)},
        'name': f'Tag{i}',
        'popularity': random.randint(0, 35)
    } for i in range(10)
]


def paginate(objects_list, request, per_page=5):
    paginator = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    objects = paginator.get_page(page)

    return objects


def index(request):
    all_new_questions = questions.copy()
    all_new_questions.reverse()
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)
    new_questions = paginate(all_new_questions, request)

    return render(request, 'index.html', {'questions': new_questions,
                                          'popular_tags': popular_tags})


def hot_questions(request):
    all_sorted_questions = questions.copy()
    all_sorted_questions.sort(key=lambda x: x.get('likes'), reverse=True)
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)
    sorted_questions = paginate(all_sorted_questions, request)

    return render(request, 'hot_questions.html', {'questions': sorted_questions,
                                                  'popular_tags': popular_tags})


def tag(request, name):
    current_tag = {}
    popular_tags = []
    for tag in tags:
        if tag.get('name') == name:
            current_tag = tag
        if tag.get('popularity') > 5:
            popular_tags.append(tag)
    current_tag_all_questions = []
    for question in questions:
        if current_tag.get('name') in question.get('tags_name'):
            current_tag_all_questions.append(question)
    current_tag_all = paginate(current_tag_all_questions, request)

    return render(request, 'tag.html', {'tag': current_tag,
                                        'questions': current_tag_all,
                                        'popular_tags': popular_tags})


def answers_for_question(request, pk):
    question = questions[pk]
    all_question_answers = []
    for answer in answers:
        if answer.get('question_id') == pk:
            all_question_answers.append(answer)
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)
    question_answers = paginate(all_question_answers, request)

    return render(request, 'question.html', {'question': question,
                                             'answers': question_answers,
                                             'popular_tags': popular_tags})


def login(request):
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)

    return render(request, 'login.html', {'popular_tags': popular_tags})


def signup(request):
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)

    return render(request, 'signup.html', {'popular_tags': popular_tags})


def ask(request):
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)

    return render(request, 'new_question.html', {'popular_tags': popular_tags})


def settings(request):
    popular_tags = []
    for tag in tags:
        if tag.get('popularity') > 5:
            popular_tags.append(tag)

    return render(request, 'settings.html', {'popular_tags': popular_tags})
