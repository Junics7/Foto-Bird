from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Sum
from django.core.validators import MinValueValidator, MaxValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(verbose_name="Описание категории")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

class Bird(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название птицы")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='birds', verbose_name="Категория")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='birds', verbose_name="Владелец")
    description = models.TextField(verbose_name="Описание птицы")
    image = models.ImageField(upload_to='birds/', verbose_name="Фотография птицы")
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    
    def __str__(self):
        return self.name
    
    def judge_score(self):
        score = JudgeEvaluation.objects.filter(bird=self).aggregate(Avg('score'))
        return score['score__avg'] or 0
    
    def visitor_votes(self):
        return VisitorVote.objects.filter(bird=self).count()
    
    def total_score(self):
        # Рассчитываем общий балл (среднее от судей + количество голосов посетителей)
        judge_avg = self.judge_score() * 10  # Умножаем на 10 для равного веса с голосами посетителей
        visitor_count = self.visitor_votes()
        return judge_avg + visitor_count
    
    class Meta:
        verbose_name = "Птица"
        verbose_name_plural = "Птицы"
        ordering = ['-submitted_at']

class VisitorVote(models.Model):
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE, related_name='visitor_votes', verbose_name="Птица")
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Посетитель")
    voted_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата голосования")
    score = models.IntegerField(default=1, verbose_name="Балл (1)")
    
    class Meta:
        verbose_name = "Голос посетителя"
        verbose_name_plural = "Голоса посетителей"
        unique_together = ('bird', 'visitor')  # Один посетитель может голосовать за одну птицу только один раз

class JudgeEvaluation(models.Model):
    bird = models.ForeignKey(Bird, on_delete=models.CASCADE, related_name='judge_evaluations', verbose_name="Птица")
    judge = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Судья")
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Оценка (1-10)"
    )
    comments = models.TextField(blank=True, verbose_name="Комментарии")
    evaluated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оценки")
    
    class Meta:
        verbose_name = "Оценка судьи"
        verbose_name_plural = "Оценки судей"
        unique_together = ('bird', 'judge')  # Один судья может оценить одну птицу только один раз
