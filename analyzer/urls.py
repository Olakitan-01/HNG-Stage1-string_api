from django.urls import path
from .views import AnalyzeStringView, StringDetailView, NaturalLanguageFilterView

urlpatterns = [
    path("/strings", AnalyzeStringView.as_view(), name="analyze_strings"),  # POST + GET
    path("/strings/filter-by-natural-language", NaturalLanguageFilterView.as_view(), name="nlp_filter"),
    path("/strings/<str:string_value>", StringDetailView.as_view(), name="string_detail"),  # GET + DELETE
]