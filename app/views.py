from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import math
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings as conf_settings
from cent import Client
from django.core.cache import cache
from faker import Faker
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.template.loader import render_to_string
import jwt
import time

from .forms import *
from .models  import *
from django.db.models import Count

faker = Faker()

client = Client(conf_settings.CENTRIFUGO_API_URL, api_key=conf_settings.CENTRIFUGO_API_KEY, timeout=1)

def get_centrifugo_data(user, channel):
    return {
        "centrifugo": {
            "token": jwt.encode({"sub": str(user.id), "exp": int(time.time()) + 10 * 60}, conf_settings.CENTRIFUGO_TOKEN_HMAC_SECRET_KEY, algorithm="HS256"),
            "ws_url": conf_settings.CENTRIFUGO_WS_URL,
            "channel": channel,
        }
    }

def search(request, search_query):
    question = Question.objects.filter(Q(content__icontains=search_query) | Q(title__icontains=search_query)).order_by("-date_writen")
    return question[:10]

def cache_pop_tags():
    cache_key = 'pop_tags'
    tags = [{"id": i, "tag": faker.name()} for i in range(6)]
    cache.set(cache_key, tags, 30)

def cache_best_members():
    cache_key = 'best_members'
    members = [{"avatar": {"url": "/ask_fedasov/media/Default.png"}, "user": {"username": faker.name()}} for i in range(6)]
    cache.set(cache_key, members, 30)

def pop_tags():
    # cache_key = 'pop_tags'
    # tags = cache.get(cache_key)
    tags = Tag.objects.annotate(q_count=Count('questions')).order_by('-q_count')[:10]
    return tags

def best_members():
    # cache_key = 'best_members'
    # users = cache.get(cache_key)
    users = Profile.objects.annotate(answer_count=Count('answer')).order_by('-answer_count')[:10]
    return users

def paginate(request, objects, page_namber, per_page=10):
    try:
        page = request.GET.get('page', page_namber)
        paginator = Paginator(objects, per_page)
        return paginator.page(page)
    except Exception as err:
        print(f"Unexpected {err}")
    return []

def index(request, page_number=1):
    search_query = request.GET.get("q")
    if search_query == None:
        QUESTIONS = Question.objects.new_question()
    else:
        QUESTIONS = search(request, search_query)
        is_ajax_request = request.headers.get("x-requested-with") == "XMLHttpRequest"
        if is_ajax_request:
            html = render_to_string(
                template_name="includes/artists-results-partial.html",
                context={"questions": QUESTIONS}
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
    return render(request, 'index.html', {'objects': paginate(request, QUESTIONS, page_number), 'pop_tags': pop_tags(),
                                          'best_members': best_members()})

def hot(request, page_number=1):
    hot_question = Question.objects.hot_question()
    return render(request, 'index.html', {'objects': paginate(request, hot_question, page_number), 'pop_tags': pop_tags(), 'best_members': best_members()})

def question(request, question_id, page_number=1):
    item = Question.objects.new_question().get(id=question_id)
    answers = Answer.objects.answer_question(question_id)
    if request.method == "GET":
        answer_form = AnswerForm(request.user, question_id)
    if request.method == "POST":
        if not request.user.is_authenticated:               #проверка на аутентификацию
            return redirect("/login")
        answer_form = AnswerForm(request.user, question_id, request.POST)
        if answer_form.is_valid():
            answer_object = answer_form.save()
            if answer_object is not None:
                dict_model = model_to_dict(answer_object)
                dict_model["url_avatar"] = answer_form.user.profile.avatar.url
                client.publish(f"question.{question_id}", dict_model)
                my_answer = Answer.objects.filter(question__id=question_id).count()
                page_number_answer = math.ceil(my_answer / 10)
                return redirect(f"%s?page={page_number_answer}" % reverse("question", args=[question_id]))
            else:
                answer_form.add_error(field=None, error="Wrong text question")
    return render(request,
                  'question.html',
                  context=
                  {
                      'question': item,
                      'objects': paginate(request, answers, page_number),
                      'form': answer_form,
                      'pop_tags': pop_tags(),
                      'best_members': best_members(),
                      **get_centrifugo_data(request.user, f"question.{question_id}")
                  }
            )

def popular_tags(request, tag_id, page_number=1):
    tag = Tag.objects.get(id=tag_id)
    question = Question.objects.top_tag_questions(tag)
    return render(request, 'index.html', {'objects': paginate(request, question, page_number), 'pop_tags': pop_tags(), 'best_members': best_members()})

@login_required(login_url='login/', redirect_field_name='continue')
def ask(request):
    if request.method == "GET":
        question_form = QuestionForm(request.user)
    if request.method == "POST":
        question_form = QuestionForm(request.user, request.POST)
        if question_form.is_valid():
            _question = question_form.save()
            if _question is not None:
                request.method = "GET"
                return redirect(reverse("question", args=[_question.id]))
            else:
                question_form.add_error(field=None, error="Wrong text question")
    return render(request, 'ask.html', context={'form': question_form, 'pop_tags': pop_tags(), 'best_members': best_members()})

@csrf_protect
def log_in(request):
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                login_form.add_error(None, "Wrong password or user does not exist")
    return render(request, 'login.html', context={'form': login_form, 'pop_tags': pop_tags(), 'best_members': best_members()})

def signup(request):
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="A user with this name already exists")
    return render(request, 'register.html', context={'form': user_form, 'pop_tags': pop_tags(), 'best_members': best_members()})

@login_required(login_url='login/', redirect_field_name='continue')
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile': profile, 'pop_tags': pop_tags(), 'best_members': best_members()})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def edit_profile(request):
    if request.method == "GET":
        form = ProfileForm(initial=model_to_dict(request.user))
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
    return render(request, 'edit_profile.html', context={'form': form, 'pop_tags': pop_tags(), 'best_members': best_members()})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def like_question(request):
    id = request.POST.get('object_id')
    # question = get_object_or_404(Question, pk=id)
    question = Question.objects.filter(pk=id).first()
    if not question:
        return JsonResponse({'status': 'fail'})
    if request.POST.get('like') == "True":
        LikeQuestion.objects.toggle_like(user=request.user.profile, question=question)
    elif request.POST.get('like') == "False":
        LikeQuestion.objects.toggle_dislike(user=request.user.profile, question=question)
    count = question.rating
    return JsonResponse({"counter": count})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def like_answer(request):
    id = request.POST.get('object_id')
    # answer = get_object_or_404(Answer, pk=id)
    answer = Answer.objects.filter(pk=id).first()
    if not answer:
        return JsonResponse({'status': 'fail'})
    if request.POST.get('like') == "True":
        LikeAnswer.objects.toggle_like(user=request.user.profile, answer=answer)
    elif request.POST.get('like') == "False":
        LikeAnswer.objects.toggle_dislike(user=request.user.profile, answer=answer)
    count = answer.rating
    return JsonResponse({"counter": count})

@csrf_protect
@login_required(login_url='login/', redirect_field_name='continue')
def answer_correct(request):
    id = request.POST.get('object_id')
    answer = Answer.objects.filter(pk=id).first()
    if not answer:
        return JsonResponse({'status': 'fail'})
    # answer = get_object_or_404(Answer, pk=id)
    if answer.correct == True:
        answer.correct = False
    else:
        answer.correct = True
    answer.save()
    return JsonResponse({"status": "OK"})

def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))

def error_404_view(request, exception):
    return render(request, 'error/404.html')