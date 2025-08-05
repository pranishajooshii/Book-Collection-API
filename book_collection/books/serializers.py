
from .models import Book, Genre,UserCollection
from rest_framework import serializers 
from django.utils import timezone

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']



class BookSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'genre','total_pages' ]
        read_only_fields = ['id','google_books_id','created_at','updated_at' ]

class UserCollectionSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    progress_percentage=serializers.SerializerMethodField()

    class Meta:
        model = UserCollection
        fields = ['id', 'user', 'book', 'reading_status', 'date_added', 'date_started', 'date_finished','progress_percentage','current_page']
        read_only_fields = ['id', 'user', 'date_added']
    

    def validate_reading_status(self, value):
        field = UserCollection._meta.get_field('reading_status')
        valid_statuses = [choice[0] for choice in field.choices]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
            )
        return value
    def validate(self, data):
        date_finished= data.get('date_finished')
        date_started = data.get('date_started')
        if date_finished and date_started and date_finished < date_started:
            raise serializers.ValidationError("Date finished cannot be before date started.")  
    
        return data
    
    def update(self, instance, validated_data):
        reading_status = validated_data.get('reading_status')

        if reading_status=='read' and not instance.date_finished:
              validated_data['date_finished'] = timezone.now()
        elif reading_status=='currently_reading' and not instance.date_started:
              validated_data['date_started'] = timezone.now()
        return super().update(instance, validated_data)

    
    def get_progress_percentage(self,obj):
        if obj.current_page and obj.book.total_pages:
            return round((obj.current_page/obj.book.total_pages)*100)
        return 0
    
    def validate_current_page(self, value):
        if value and hasattr(self.instance, 'book'):
            if value > self.instance.book.total_pages:
                raise serializers.ValidationError(
                    f"Current page cannot exceed total pages ({self.instance.book.total_pages})"
                )
        return value