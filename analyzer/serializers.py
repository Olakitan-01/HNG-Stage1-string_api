from rest_framework import serializers
from .models import AnalyzedString


class AnalyzeInputSerializer(serializers.Serializer):
    value = serializers.CharField(required=True)


class PropertiesSerializer(serializers.Serializer):
    length = serializers.IntegerField()
    is_palindrome = serializers.BooleanField()
    unique_characters = serializers.IntegerField()
    word_count = serializers.IntegerField()
    sha256_hash = serializers.CharField()
    character_frequency_map = serializers.DictField(child=serializers.IntegerField())


class AnalyzedStringSerializer(serializers.ModelSerializer):
    properties = PropertiesSerializer(source="*")

    class Meta:
        model = AnalyzedString
        fields = ("id", "value", "properties", "created_at")
        read_only_fields = ("id", "created_at")

    def to_representation(self, instance):
        return instance.to_dict()