from django.shortcuts import render
from .models import Genre, Book, UserCollection
from .serializers import GenreSerializer, BookSerializer, UserCollectionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import os
import requests
from django.utils import timezone

# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_google_books(request):
    query = request.GET.get('q', '')
    if not query:
        return Response({"error": "Query parameter 'q' is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    api_key = os.getenv('GOOGLE_BOOKS_API_KEY')
    if not api_key:
        return Response({"error": "Google Books API key not configured"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    try:
        response = requests.get(
            "https://www.googleapis.com/books/v1/volumes",
            params={
                'q': query,
                'maxResults': 10,
                'key': api_key
            },
            timeout=5
        )
        response.raise_for_status()
        
       
        books_data = response.json()
        simplified_results = []
        
        for item in books_data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            simplified_results.append({
                'google_book_id': item.get('id'),
                'author': ', '.join(volume_info.get('authors', ['Unknown'])),
                'total_pages': volume_info.get('pageCount'),
                'genres': volume_info.get('categories', [])
            })
        
        return Response(simplified_results)
        
    except requests.exceptions.RequestException as e:
        return Response(
            {"error": f"Google Books API request failed: {str(e)}"},
            status=status.HTTP_502_BAD_GATEWAY
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_collection(request):
    user= request.user
    reading_status = request.data.get('reading_status')
    book_data = request.data.get('book_data')

    if not reading_status or not book_data:
        return Response({"error": "Shelf ID and book data are required"}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        book,created=Book.objects.get_or_create(
            google_books_id=book_data.get('google_book_id'),
            defaults={
                'name': book_data.get('title', 'Unknown Title'),
                'author': ', '.join(book_data.get('authors', ['Unknown'])),
                'total_pages': book_data.get('pageCount', 0)
            }
        )

        if created and 'categories' in book_data:
            for genre_name in book_data['categories']:
                genre, _ = Genre.objects.get_or_create(name=genre_name)
                book.genre.add(genre)
        
        collection, created = UserCollection.objects.update_or_create(
            user=user,
            book=book,
            defaults={
                'reading_status': reading_status,
                'date_started': timezone.now() if reading_status == 'currently_reading' else None,
                'date_finished': timezone.now() if reading_status == 'read' else None
            }
        )

        return Response({
        "message": "Book added successfully",
        "collection": UserCollectionSerializer(collection).data,
        "book": BookSerializer(book).data
    }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_collection(request):
    collections = UserCollection.objects.filter(user=request.user)
    serializer = UserCollectionSerializer(collections, many=True)
    return Response(serializer.data)