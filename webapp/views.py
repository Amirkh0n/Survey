from django.shortcuts import render, get_object_or_404, redirect
from modelapp.models import Survey, Answer, AnswerItem
from .forms import SurveyForm
import json  # agar checkbox uchun JSON saqlashni xohlasang

# --- Survey ni ko‘rsatish + javob qabul qilish ---
def survey_detail(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)

    if request.method == "POST":
        form = SurveyForm(request.POST, survey=survey)
        if form.is_valid():
            # Javob konteynerini yaratish
            answer = Answer.objects.create(survey=survey)

            # Har bir savolga AnswerItem yaratish
            for field_name, value in form.cleaned_data.items():
                q_id = int(field_name.split("_")[1])
                question = survey.questions.get(id=q_id)

                # Checkbox bo‘lsa list bo‘ladi → JSON yoki CSV saqlash mumkin
                if question.type == "checkbox":
                    value = json.dumps(value)  # JSON formatida saqlash

                AnswerItem.objects.create(
                    answer=answer,
                    question=question,
                    value=value
                )

            return redirect("thank_you")
    else:
        form = SurveyForm(survey=survey)

    return render(request, "survey_form.html", {
        "survey": survey,
        "form": form
    })


# --- Thank you page ---
def thank_you(request):
    return render(request, "thank_you.html")


# --- Optional: Survey list page ---
def survey_list(request):
    surveys = Survey.objects.all()
    return render(request, "survey_list.html", {"surveys": surveys})