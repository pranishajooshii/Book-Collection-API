
from .models import Book, Genre,UserCollection
from rest_framework import serializers as serializer
class GenreSerializer(serializer.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']



class BookSerializer(serializer.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'genre','total_pages' ]
        read_only_fields = ['id','google_books_id','created_at','updated_at' ]

class UserCollectionSerializer(serializer.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = UserCollection
        fields = ['id', 'user', 'book', 'reading_status', 'date_added', 'date_started', 'date_finished']
        read_only_fields = ['id', 'user', 'date_added']