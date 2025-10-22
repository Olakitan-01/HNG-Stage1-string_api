from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AnalyzedString
from .serializers import AnalyzeInputSerializer, AnalyzedStringSerializer
from .utils import compute_sha256

class AnalyzeStringView(APIView):
    """Handles POST /strings and GET /strings"""

    def post(self, request):
        serializer = AnalyzeInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Missing or invalid 'value' field"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        value = serializer.validated_data["value"]
        if AnalyzedString.objects.filter(value=value).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        analyzed = AnalyzedString.objects.create(value=value)
        return Response(AnalyzedStringSerializer(analyzed).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        qs = AnalyzedString.objects.all()
        params = request.query_params

        is_palindrome = params.get("isPalindrome")
        length = params.get("length")

        if is_palindrome is not None:
            qs = qs.filter(is_palindrome=is_palindrome.lower() == "true")
        if length is not None:
            try:
                qs = qs.filter(value__len=int(length))
            except ValueError:
                return Response({"error": "Invalid length"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StringDetailView(APIView):
    """Handles GET /strings/<string_value> and DELETE /strings/<string_value>"""

    def get(self, request, string_value):
        analyzed = get_object_or_404(AnalyzedString, value=string_value)
        return Response(AnalyzedStringSerializer(analyzed).data, status=status.HTTP_200_OK)

    def delete(self, request, string_value):
        analyzed = AnalyzedString.objects.filter(value=string_value).first()
        if not analyzed:
            return Response({"error": "String not found"}, status=status.HTTP_404_NOT_FOUND)
        analyzed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class NaturalLanguageFilterView(APIView):
    """Handles GET /strings/filter-by-natural-language"""

    def get(self, request):
        query = request.query_params.get("query")
        if not query:
            return Response({"error": "Missing query parameter"}, status=status.HTTP_400_BAD_REQUEST)

        query_lower = query.lower()
        qs = AnalyzedString.objects.all()

        if "palindrome" in query_lower:
            qs = qs.filter(is_palindrome=True)
        if "length" in query_lower:
            try:
                num = int("".join(filter(str.isdigit, query_lower)))
                qs = qs.filter(value__len=num)
            except ValueError:
                pass
        elif "longer than" in query_lower:
            try:
                num = int("".join(filter(str.isdigit, query_lower)))
                qs = qs.filter(value__len__gt=num)
            except ValueError:
                pass

        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)