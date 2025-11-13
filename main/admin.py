from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import (
    UserProfile, ParentProfile, TeacherProfile, PsychologistProfile,
    Child, TestQuestion, TestResult
)
def export_as_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name_plural}.csv'
    writer = csv.writer(response)
    # Write header
    field_names = [field.name for field in opts.fields]
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response

export_as_csv.short_description = "Export selected items to CSV"

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type', 'created_at')
    list_filter = ('user_type', 'created_at')
    search_fields = ('user__username', 'user__email')
    actions = [export_as_csv]

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'parent_type')
    list_filter = ('parent_type',)
    actions = [export_as_csv]

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'school_name')
    search_fields = ('school_name',)
    actions = [export_as_csv]

@admin.register(PsychologistProfile)
class PsychologistProfileAdmin(admin.ModelAdmin):
    list_display = ('user_profile', 'professional_qualification', 'organization_clinic')
    search_fields = ('professional_qualification', 'organization_clinic')
    actions = [export_as_csv]

@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'grade', 'school_name', 'created_at')
    list_filter = ('age', 'grade', 'created_at')
    search_fields = ('name', 'school_name')
    actions = [export_as_csv]

@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_number', 'category', 'question_text')
    list_filter = ('category',)
    ordering = ('question_number',)
    actions = [export_as_csv]

@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ('child', 'user', 'test_date', 'has_ld', 'has_dyslexia', 'has_dysgraphia', 'has_dyscalculia')
    list_filter = ('has_ld', 'has_dyslexia', 'has_dysgraphia', 'has_dyscalculia', 'has_psychological_impact', 'test_date')
    search_fields = ('child__name', 'user__username')
    readonly_fields = ('test_date', 'total_score', 'dyslexia_score', 'dysgraphia_score', 'dyscalculia_score', 'psychological_score')
    actions = [export_as_csv]