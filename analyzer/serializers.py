from rest_framework import serializers
from .models import AnalyzedString

class AnalyzeInputSerializer(serializers.Serializer):
    value = serializers.CharField(required=True, allow_blank=False)

    def validate_value(self, value):
        if not isinstance(value, str):
            raise serializers.ValidationError("Value must be a string")
        return value

class AnalyzedStringSerializer(serializers.ModelSerializer):
    hash = serializers.CharField(source="sha256_hash")

    class Meta:
        model = AnalyzedString
        fields = ("value", "hash", "is_palindrome")

    def to_representation(self, instance):
        return instance.to_dict()