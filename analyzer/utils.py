import hashlib
import collections




def compute_sha256(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("value must be a string")
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def get_length(value: str) -> int:
    return len(value)


def is_palindrome(value: str) -> bool:
    s = value.lower()
    return s == s[::-1]

def count_unique_characters(value: str) -> int:
    return len(set(value))


def word_count(value: str) -> int:
    parts = value.split()
    return len(parts)


def character_frequency_map(value: str) -> dict:
    return dict(collections.Counter(value))