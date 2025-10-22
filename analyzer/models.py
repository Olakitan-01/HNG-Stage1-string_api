from django.db import models
import hashlib

class AnalyzedString(models.Model):
    value = models.TextField(unique=True)
    sha256_hash = models.CharField(max_length=64, unique=True, editable=False)
    is_palindrome = models.BooleanField(editable=False)

    def save(self, *args, **kwargs):
        # Compute SHA-256 hash
        self.sha256_hash = hashlib.sha256(self.value.encode("utf-8")).hexdigest()
        # Case-insensitive palindrome check
        self.is_palindrome = self.value.lower() == self.value.lower()[::-1]
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            "value": self.value,
            "hash": self.sha256_hash,
            "is_palindrome": self.is_palindrome,
        }

    class Meta:
        ordering = ["-id"]