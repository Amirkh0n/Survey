from django.urls import path
from . import views

urlpatterns = [
    path("", views.survey_list, name="survey_list"),
    path("survey/<int:survey_id>/", views.survey_detail, name="survey_detail"),
    path("thanks/", views.thank_you, name="thank_you"),
]