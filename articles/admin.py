from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        tags = {}
        for form in self.forms:
            form.cleaned_data
            if form.cleaned_data.get('tag') is not None:
                tags[form.cleaned_data.get('tag')] = form.cleaned_data.get('is_main')
        choices = list(tags.values()).count(True)
        if choices == 0:
            raise ValidationError('Укажите основной раздел')
        elif choices > 1:
            raise ValidationError('Основным может быть только один раздел')

        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'published_at', 'image']
    inlines = [ScopeInline]


@admin.register(Tag)
class ScopeAdmin(admin.ModelAdmin):
    list_display = ['name']
