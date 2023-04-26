from datetime import datetime

from rest_framework import serializers
from .models import Book, Author, Publisher, Buyer, BuyerSubscription


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'

    def validate_age(self, value):
        if not 18 <= value <= 100:
            raise serializers.ValidationError('Publisher age must be between 18 and 100.')
        return value


class BuyerSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerSubscription
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

    def validate_year_published(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError('Year published cannot be in the future.')
        return value


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = '__all__'

    def validate_email(self, value):
        if Buyer.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email address is already in use.')
        return value


class PublisherStatsDTOSerializer(serializers.Serializer):
    publisher_name = serializers.CharField()
    average_number_of_pages = serializers.FloatField()


class AuthorStatsDTOSerializer(serializers.Serializer):
    author_first_name = serializers.CharField()
    average_number_of_pages = serializers.FloatField()
