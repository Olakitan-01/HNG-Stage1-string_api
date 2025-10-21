from django.urls import path
from .views import (
    CreateAnalyzeStringView,
    GetStringView,
    ListStringsView,
    NaturalLanguageFilterView,
    DeleteStringView,
)

urlpatterns = [
    path("strings", CreateAnalyzeStringView.as_view(), name="create_string"),
    path("strings/", ListStringsView.as_view(), name="list_strings"),
    path("strings/filter-by-natural-language", NaturalLanguageFilterView.as_view(), name="nlp_filter"),
    path("strings/<str:string_value>", GetStringView.as_view(), name="get_string"),
    path("strings/<str:string_value>/delete", DeleteStringView.as_view(), name="delete_string"),
]
