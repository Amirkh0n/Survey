from django.contrib import admin
from .models import Survey, Question, Option, Answer, AnswerItem


# -------------------------------
#   Inline: Option (Radio/Select/Checkbox variantlari)
# -------------------------------
class OptionInline(admin.TabularInline):
    model = Option
    extra = 1
    min_num = 0


# -------------------------------
#   Inline: Question (So‘rovnoma ichidagi savollar)
# -------------------------------
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1
    show_change_link = True
    ordering = ('order',)
    fields = ('text', 'type', 'required', 'order')
    inlines = []


# -------------------------------
#   Survey Admin
# -------------------------------
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    inlines = [QuestionInline]


# -------------------------------
#   Question Admin (variantlar ko‘rsatiladi)
# -------------------------------
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'type', 'survey', 'order')
    list_filter = ('survey', 'type')
    search_fields = ('text',)
    ordering = ('survey', 'order')
    inlines = [OptionInline]


# -------------------------------
#   AnswerItem Inline (har bir savol javobi)
# -------------------------------
class AnswerItemInline(admin.TabularInline):
    model = AnswerItem
    readonly_fields = ('question', 'value')
    extra = 0
    can_delete = False


# -------------------------------
#   Answer Admin (foydalanuvchi yuborgan to‘liq forma)
# -------------------------------
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'survey', 'submitted_at')
    list_filter = ('survey',)
    readonly_fields = ('survey', 'submitted_at')
    inlines = [AnswerItemInline]

    def has_add_permission(self, request):
        # Admin qo‘lda answer qo‘shmasligi kerak → faqat foydalanuvchi yuboradi
        return False


# -------------------------------
#   AnswerItem Admin (odatda keraksiz → yashirib qo‘yamiz)
# -------------------------------
@admin.register(AnswerItem)
class AnswerItemAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'value')
    readonly_fields = ('answer', 'question', 'value')

    def has_add_permission(self, request):
        return False