from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Author, Book, Buyer, Purchase, Publisher, PublisherStatsDTO
from .serializer import BookSerializer, PublisherStatsDTOSerializer
from django.db.models import Avg

class NonCrudFunctionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.author = Author.objects.create(first_name="John", last_name="Doe", birth_date="2000-01-01", email="john@example.com", website="https://www.example.com")
        self.publisher1 = Publisher.objects.create(name="Publisher 1", address="123 Main St", city="New York", country="USA", website="https://www.publisher1.com", age=20)
        self.publisher2 = Publisher.objects.create(name="Publisher 2", address="456 Elm St", city="Los Angeles", country="USA", website="https://www.publisher2.com", age=25)
        self.book1 = Book.objects.create(title="Test Book 1", number_of_pages=100, publish_date="2022-01-01", quantity=10, ibn=12345, author=self.author, publisher=self.publisher1, price=100)
        self.book2 = Book.objects.create(title="Test Book 2", number_of_pages=200, publish_date="2022-02-01", quantity=20, ibn=12346, author=self.author, publisher=self.publisher2, price=200)

    def test_publisher_stats_dto_serializer(self):
        # Create a PublisherStatsDTO instance
        publisher_stats = PublisherStatsDTO(publisher_name='Oxford University Press', average_number_of_pages=256)

        # Serialize the instance to JSON using the PublisherStatsDTOSerializer
        serializer = PublisherStatsDTOSerializer(publisher_stats)
        serialized_data = serializer.data

        # Test the serialized data
        expected_data = {'publisher_name': 'Oxford University Press', 'average_number_of_pages': 256.0}
        self.assertEqual(serialized_data, expected_data)

    def test_books_with_pages_above(self):
        min_pages = 150
        response = self.client.get(reverse('books_with_pages_above', kwargs={'min_pages': min_pages}))
        self.assertEqual(response.status_code, 200)

        # Filter books with number_of_pages greater than or equal to min_pages
        books = Book.objects.filter(number_of_pages__gte=min_pages)
        expected_response_data = BookSerializer(books, many=True).data
        self.assertEqual(response.data, expected_response_data)
