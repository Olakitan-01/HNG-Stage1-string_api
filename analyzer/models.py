from django.db import models
import hashlib
from collections import Counter
from django.utils import timezone

class AnalyzedString(models.Model):
    value = models.TextField(unique=True)
    sha256_hash = models.CharField(max_length=64, unique=True, editable=False)
    is_palindrome = models.BooleanField(editable=False)
    created_at = models.DateTimeField(default=timezone.now)  # ✅ added timestamp

    def save(self, *args, **kwargs):
        # Compute SHA-256 hash
        self.sha256_hash = hashlib.sha256(self.value.encode("utf-8")).hexdigest()
        # Case-insensitive palindrome check
        self.is_palindrome = self.value.lower() == self.value.lower()[::-1]
        super().save(*args, **kwargs)

    def to_dict(self):
        text = self.value
        char_freq = dict(Counter(text))

        return {
            "id": self.sha256_hash,  # ✅ id is the hash
            "value": text,
            "properties": {
                "length": len(text),
                "is_palindrome": self.is_palindrome,
                "unique_characters": len(set(text)),
                "word_count": len(text.split()),
                "sha256_hash": self.sha256_hash,
                "character_frequency_map": char_freq,
            },
            "created_at": self.created_at.isoformat() + "Z",  # ✅ ISO timestamp
        }

    class Meta:
        ordering = ["-created_at"]
