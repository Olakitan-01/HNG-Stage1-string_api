from django.db import models

# Create your models here.
class AnalyzedString(models.Model):
    id = models.CharField(max_length=64, primary_key=True) # sha256 hex
    value = models.TextField()
    length = models.IntegerField()
    is_palindrome = models.BooleanField()
    unique_characters = models.IntegerField()
    word_count = models.IntegerField()
    sha256_hash = models.CharField(max_length=64, unique=True)
    character_frequency_map = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


    def properties(self):
        return {
            "length": self.length,
            "is_palindrome": self.is_palindrome,
            "unique_characters": self.unique_characters,
            "word_count": self.word_count,
            "sha256_hash": self.sha256_hash,
            "character_frequency_map": self.character_frequency_map,
        }


    def to_dict(self):
        return {
            "id": self.sha256_hash,
            "value": self.value,
            "properties": self.properties(),
            "created_at": self.created_at.isoformat(),
        }
    