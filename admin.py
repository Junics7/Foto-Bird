from django.contrib import admin
from .models import Category, Bird, VisitorVote, JudgeEvaluation

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Bird)
class BirdAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'owner', 'submitted_at')
    list_filter = ('category', 'submitted_at')
    search_fields = ('name', 'description', 'owner__username')
    readonly_fields = ('submitted_at',)

@admin.register(VisitorVote)
class VisitorVoteAdmin(admin.ModelAdmin):
    list_display = ('bird', 'visitor', 'voted_at')
    list_filter = ('voted_at',)
    search_fields = ('bird__name', 'visitor__username')
    readonly_fields = ('voted_at',)

@admin.register(JudgeEvaluation)
class JudgeEvaluationAdmin(admin.ModelAdmin):
    list_display = ('bird', 'judge', 'score', 'evaluated_at')
    list_filter = ('score', 'evaluated_at')
    search_fields = ('bird__name', 'judge__username', 'comments')
    readonly_fields = ('evaluated_at',)
