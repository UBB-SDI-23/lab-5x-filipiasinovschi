from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField()
    website = models.URLField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website = models.URLField()
    age = models.IntegerField(default=20)

    def __str__(self):
        return self.name


class Buyer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class BuyerSubscription(models.Model):
    buyer = models.OneToOneField(Buyer, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.buyer.name}'s subscription"


class Book(models.Model):
    title = models.CharField(max_length=100)
    number_of_pages = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    publish_date = models.DateField()
    quantity = models.IntegerField()
    ibn = models.IntegerField()
    # One-to-many relationship with Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    # One-to-many relationship with Publisher
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, null=True)
    # One-to-many relationship with Buyer
    buyers = models.ManyToManyField(Buyer)
    price = models.IntegerField(default=100)

    def __str__(self):
        return self.title


class PublisherStatsDTO:
    def __init__(self, publisher_name, average_number_of_pages):
        self.publisher_name = publisher_name
        self.average_number_of_pages = average_number_of_pages


class AuthorStatsDTO:
    def __init__(self, author_first_name, average_number_of_pages):
        self.author_first_name = author_first_name
        self.average_number_of_pages = average_number_of_pages


class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    price = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
