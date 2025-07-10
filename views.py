from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.core.paginator import Paginator
from django.contrib.auth import login
from .models import Category, Bird, VisitorVote, JudgeEvaluation
from .forms import BirdUploadForm, JudgeEvaluationForm, VisitorVoteForm, UserRegistrationForm

def home(request):
    # Получаем последние добавленные птицы
    latest_birds = Bird.objects.order_by('-submitted_at')[:6]
    # Получаем топ птиц по оценке судей
    top_judge_birds = sorted(Bird.objects.all(), key=lambda b: b.judge_score(), reverse=True)[:3]
    # Получаем топ птиц по голосам посетителей
    top_visitor_birds = sorted(Bird.objects.all(), key=lambda b: b.visitor_votes(), reverse=True)[:3]
    
    return render(request, 'home.html', {
        'latest_birds': latest_birds,
        'top_judge_birds': top_judge_birds,
        'top_visitor_birds': top_visitor_birds
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    birds = category.birds.all()
    
    # Пагинация
    paginator = Paginator(birds, 9)  # По 9 птиц на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'category_detail.html', {
        'category': category,
        'page_obj': page_obj
    })

def bird_detail(request, bird_id):
    bird = get_object_or_404(Bird, id=bird_id)
    judge_form = None
    judge_evaluation = None
    
    # Проверяем, может ли пользователь голосовать за эту птицу
    can_vote = False
    has_voted = False
    
    if request.user.is_authenticated:
        # Нельзя голосовать за свою птицу
        if bird.owner != request.user:
            can_vote = True
            # Проверяем, голосовал ли уже
            if VisitorVote.objects.filter(bird=bird, visitor=request.user).exists():
                has_voted = True
                can_vote = False
    
    if request.user.is_authenticated and request.user.groups.filter(name='Judges').exists():
        judge_evaluation = JudgeEvaluation.objects.filter(judge=request.user, bird=bird).first()
        if not judge_evaluation:
            judge_form = JudgeEvaluationForm()
        else:
            judge_form = JudgeEvaluationForm(instance=judge_evaluation)
    
    vote_form = VisitorVoteForm(initial={'bird_id': bird.id})
    
    return render(request, 'bird_detail.html', {
        'bird': bird,
        'can_vote': can_vote,
        'has_voted': has_voted,
        'vote_form': vote_form,
        'judge_form': judge_form,
        'judge_evaluation': judge_evaluation
    })

@login_required
def upload_bird(request):
    if request.method == 'POST':
        form = BirdUploadForm(request.POST, request.FILES)
        if form.is_valid():
            bird = form.save(commit=False)
            bird.owner = request.user
            bird.save()
            messages.success(request, 'Ваша птица успешно добавлена на выставку!')
            return redirect('bird_detail', bird_id=bird.id)
    else:
        form = BirdUploadForm()
    
    return render(request, 'upload_bird.html', {'form': form})

@login_required
def visitor_vote(request):
    if request.method == 'POST':
        form = VisitorVoteForm(request.POST)
        if form.is_valid():
            bird_id = form.cleaned_data['bird_id']
            bird = get_object_or_404(Bird, id=bird_id)
            
            # Проверка, не голосовал ли уже за птицу в этой категории
            try:
                vote = VisitorVote(bird=bird, visitor=request.user, score=1)
                vote.save()
                messages.success(request, 'Ваш голос учтен! Спасибо за участие.')
            except IntegrityError:
                messages.error(request, 'Вы уже голосовали в этой категории.')
            
            return redirect('bird_detail', bird_id=bird_id)
    
    return redirect('category_list')

@login_required
def judge_evaluate(request, bird_id):
    # Проверка, является ли пользователь судьей
    if not request.user.groups.filter(name='Judges').exists():
        messages.error(request, 'Только судьи могут оценивать птиц.')
        return redirect('bird_detail', bird_id=bird_id)
    
    bird = get_object_or_404(Bird, id=bird_id)
    
    if request.method == 'POST':
        # Проверяем, существует ли уже оценка от этого судьи
        evaluation, created = JudgeEvaluation.objects.get_or_create(
            judge=request.user,
            bird=bird,
            defaults={'score': 1, 'comments': ''}
        )
        
        form = JudgeEvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Оценка успешно сохранена!')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    
    return redirect('bird_detail', bird_id=bird_id)

@login_required
def judge_dashboard(request):
    # Проверка, является ли пользователь судьей
    if not request.user.groups.filter(name='Judges').exists():
        messages.error(request, 'Доступ запрещен.')
        return redirect('home')
    
    categories = Category.objects.all()
    
    # Получаем список птиц, которых судья еще не оценил
    unevaluated_birds = {}
    evaluated_birds = {}
    
    for category in categories:
        unevaluated_birds[category] = []
        evaluated_birds[category] = []
        
        birds = category.birds.all()
        for bird in birds:
            if JudgeEvaluation.objects.filter(judge=request.user, bird=bird).exists():
                evaluated_birds[category].append(bird)
            else:
                unevaluated_birds[category].append(bird)
    
    return render(request, 'judge_dashboard.html', {
        'categories': categories,
        'unevaluated_birds': unevaluated_birds,
        'evaluated_birds': evaluated_birds
    })

def results(request):
    categories = Category.objects.all()
    results_by_category = {}
    
    for category in categories:
        birds = category.birds.all()
        # Сортируем по общему баллу (судьи + посетители)
        sorted_birds = sorted(birds, key=lambda b: b.total_score(), reverse=True)
        results_by_category[category] = sorted_birds
    
    return render(request, 'results.html', {
        'categories': categories,
        'results_by_category': results_by_category
    })
