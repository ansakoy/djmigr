from django.db import models


class Entry(models.Model):
    """Blog entry
    """
    title = models.CharField(
        "Title",
        max_length=1000,
        default="...",
    )
    content = models.TextField(
        "Content",
        max_length=5000,
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    """Blog comment
    """
    entry = models.ForeignKey(
        Entry,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        "Text",
        max_length=5000,
    )
