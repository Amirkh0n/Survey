from django import forms
from modelapp.models import Survey, Question, Option

class SurveyForm(forms.Form):
    """
    Zamonaviy Survey Form
    """
    def __init__(self, *args, **kwargs):
        survey = kwargs.pop("survey")
        super().__init__(*args, **kwargs)

        for question in survey.questions.all():
            field_name = f"question_{question.id}"

            field_kwargs = {
                "label": question.text,
                "required": question.required,
            }

            if question.type == "text":
                self.fields[field_name] = forms.CharField(
                    widget=forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Javobingizni kiriting..."
                    }),
                    **field_kwargs
                )

            elif question.type == "number":
                self.fields[field_name] = forms.IntegerField(
                    widget=forms.NumberInput(attrs={
                        "class": "form-control",
                        "placeholder": "Raqam kiriting..."
                    }),
                    **field_kwargs
                )

            elif question.type == "textarea":
                self.fields[field_name] = forms.CharField(
                    widget=forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 4,
                        "placeholder": "Batafsil javob yozing..."
                    }),
                    **field_kwargs
                )

            elif question.type == "radio":
                choices = [(opt.id, opt.text) for opt in question.options.all()]
                self.fields[field_name] = forms.ChoiceField(
                    widget=forms.RadioSelect(),
                    choices=choices,
                    **field_kwargs
                )
                
            elif question.type == "checkbox":
                choices = [(opt.id, opt.text) for opt in question.options.all()]
                self.fields[field_name] = forms.MultipleChoiceField(
                    widget=forms.CheckboxSelectMultiple(),
                    choices=choices,
                    **field_kwargs
                )
                
            elif question.type == "select":
                choices = [(opt.id, opt.text) for opt in question.options.all()]
                self.fields[field_name] = forms.ChoiceField(
                    widget=forms.Select(attrs={
                        "class": "form-select"
                    }),
                    choices=[("", "Tanlang...")] + choices,
                    **field_kwargs
                )
