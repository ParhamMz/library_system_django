from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, editable=False)

    def __str__(self) -> str:
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    author = models.CharField(max_length=50)
    translator = models.CharField(max_length=50, blank=True, null=True)
    publisher = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    pages = models.PositiveIntegerField()
    publication_year = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    available_numbers = models.PositiveIntegerField(default=3)
    book_imgs = models.ImageField(upload_to='books_cover', default='books_cover/unknown-book.jpeg', blank=True, null=True)
    book_pdf = models.FileField(upload_to='books_files', blank=True, null=True)
    free = models.BooleanField(default=True)
    lent_by = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title

