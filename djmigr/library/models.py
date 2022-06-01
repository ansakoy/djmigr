from django.db import models


class Author(models.Model):
    """Author
    """
    full_name = models.CharField(
        "Author's name",
        max_length=500,
    )
    birth_date = models.DateField(
        "Date of birth",
        null=True,
        default=None,
        blank=True,
    )

    def __str__(self):
        return self.full_name


class Book(models.Model):
    """Book
    """
    title = models.CharField(
        "Title",
        max_length=1000,
    )
    author = models.ForeignKey(
        Author,
        related_name="books",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    publish_year = models.IntegerField(
        "Publication year",
        null=True,
        blank=True,
        default=None,
    )

    def __str__(self):
        return self.title
