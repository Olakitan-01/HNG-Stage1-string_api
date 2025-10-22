from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import AnalyzedString
from .serializers import AnalyzeInputSerializer, AnalyzedStringSerializer
from .utils import (
    compute_sha256,
    get_length,
    is_palindrome,
    count_unique_characters,
    word_count,
    character_frequency_map,
)


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
        sha_hash = compute_sha256(value)

        if AnalyzedString.objects.filter(id=sha_hash).exists():
            return Response({"error": "String already exists"}, status=status.HTTP_409_CONFLICT)

        analyzed = AnalyzedString.objects.create(
            id=sha_hash,
            value=value,
            length=get_length(value),
            is_palindrome=is_palindrome(value),
            unique_characters=count_unique_characters(value),
            word_count=word_count(value),
            sha256_hash=sha_hash,
            character_frequency_map=character_frequency_map(value),
        )

        return Response(AnalyzedStringSerializer(analyzed).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        qs = AnalyzedString.objects.all()
        params = request.query_params

        is_palindrome_param = params.get("is_palindrome")
        min_length = params.get("min_length")
        max_length = params.get("max_length")
        word_count_param = params.get("word_count")
        contains_character = params.get("contains_character")

        if is_palindrome_param is not None:
            qs = qs.filter(is_palindrome=is_palindrome_param.lower() == "true")
        if min_length is not None:
            qs = qs.filter(length__gte=int(min_length))
        if max_length is not None:
            qs = qs.filter(length__lte=int(max_length))
        if word_count_param is not None:
            qs = qs.filter(word_count=int(word_count_param))
        if contains_character is not None:
            qs = qs.filter(value__icontains=contains_character)

        serializer = AnalyzedStringSerializer(qs, many=True)
        return Response(
            {
                "data": serializer.data,
                "count": qs.count(),
                "filters_applied": dict(params),
            },
            status=status.HTTP_200_OK,
        )


class StringDetailView(APIView):
    """Handles GET /strings/<string_value> and DELETE /strings/<string_value>"""

    def get(self, request, string_value):
        sha_hash = compute_sha256(string_value)
        analyzed = get_object_or_404(AnalyzedString, id=sha_hash)
        return Response(AnalyzedStringSerializer(analyzed).data, status=status.HTTP_200_OK)

    def delete(self, request, string_value):
        sha_hash = compute_sha256(string_value)
        analyzed = AnalyzedString.objects.filter(id=sha_hash).first()
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
        filters = {}

        if "palindromic" in query_lower:
            filters["is_palindrome"] = True
        if "single word" in query_lower:
            filters["word_count"] = 1
        if "longer than" in query_lower:
            try:
                num = int("".join(filter(str.isdigit, query_lower)))
                filters["min_length"] = num + 1
            except ValueError:
                pass
        if "containing the letter" in query_lower:
            for char in query_lower.split():
                if len(char) == 1 and char.isalpha():
                    filters["contains_character"] = char
                    break

        if not filters:
            return Response({"error": "Unable to parse natural language query"}, status=status.HTTP_400_BAD_REQUEST)

        qs = AnalyzedString.objects.all()
        if "is_palindrome" in filters:
            qs = qs.filter(is_palindrome=True)
        if "word_count" in filters:
            qs = qs.filter(word_count=filters["word_count"])
        if "min_length" in filters:
            qs = qs.filter(length__gte=filters["min_length"])
        if "contains_character" in filters:
            qs = qs.filter(value__icontains=filters["contains_character"])

        data = AnalyzedStringSerializer(qs, many=True).data
        return Response(
            {
                "data": data,
                "count": len(data),
                "interpreted_query": {"original": query, "parsed_filters": filters},
            },
            status=status.HTTP_200_OK,
        )
