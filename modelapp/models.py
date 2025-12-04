from django.db import models
from django.utils import timezone


# -------------------------------
#   1. SURVEY (So‘rovnoma)
# -------------------------------
class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# -------------------------------
#   2. QUESTION (Savollar)
# -------------------------------
class Question(models.Model):

    # Savol turlari
    TEXT = 'text'
    NUMBER = 'number'
    TEXTAREA = 'textarea'
    RADIO = 'radio'
    CHECKBOX = 'checkbox'
    SELECT = 'select'

    QUESTION_TYPES = [
        (TEXT, "Text"),
        (NUMBER, "Number"),
        (TEXTAREA, "Textarea"),
        (RADIO, "Radio"),
        (CHECKBOX, "Checkbox"),
        (SELECT, "Select"),
    ]

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=20, choices=QUESTION_TYPES, default=TEXT)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.text} ({self.type})"


# -------------------------------
#   3. OPTION (Variantlar)
# -------------------------------
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


# -------------------------------
#   4. ANSWER (Foydalanuvchi yuborgan javoblar)
# -------------------------------
class Answer(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='answers')
    submitted_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Answer #{self.id} → {self.survey.title}"


# -------------------------------
#   5. ANSWER ITEM (Har bir savolning javobi)
# -------------------------------
class AnswerItem(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='items')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    value = models.TextField()

    # Checkbox varianti bo‘lsa bu value JSON bo‘ladi (stringda saqlanadi)

    def __str__(self):
        return f"{self.question.text}: {self.value}"