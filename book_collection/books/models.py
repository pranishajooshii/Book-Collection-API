from django.db import models

# Create your models here.

class Genre(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    


class Book(models.Model):
    name=models.CharField(max_length=100)
    author=models.CharField(max_length=250)
    genre=models.ManyToManyField(Genre)
    total_pages=models.PositiveIntegerField(null=True, blank=True)
    google_books_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class UserCollection(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reading_status = models.CharField(
        max_length=20,
        choices=[
            ('want_to_read', 'Want to Read'),
            ('currently_reading', 'Currently Reading'),
            ('read', 'Read')
        ],
        default='want_to_read'
    )
    date_added = models.DateTimeField(auto_now_add=True)
    date_started = models.DateTimeField(null=True, blank=True)
    date_finished = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.fullname} - {self.book.name}"