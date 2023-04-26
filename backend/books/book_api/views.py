import datetime

from django.db.models import Avg, Case, ExpressionWrapper, F, fields, When
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Book, Author, Publisher, Buyer, BuyerSubscription, PublisherStatsDTO, Purchase, AuthorStatsDTO
from .serializer import BookSerializer, AuthorSerializer, PublisherSerializer, BuyerSerializer, \
    BuyerSubscriptionSerializer, PublisherStatsDTOSerializer, AuthorStatsDTOSerializer


# Create your views here.
# responsible for logic to create or return data
# books/list


@api_view(['GET'])
def books_list(request):
    books = Book.objects.all()  # complex data
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def book_create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        book = serializer.save()

        buyer_ids = request.data.get('buyers', [])
        purchases = []
        for buyer_id in buyer_ids:
            buyer = get_object_or_404(Buyer, id=buyer_id)
            purchase = Purchase(book=book, buyer=buyer, price=book.price)
            purchases.append(purchase)

        Purchase.objects.bulk_create(purchases)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except:
        return Response({'error': 'Book does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        data = serializer.data

        # Get the author and publisher objects and add them to the response
        if book.author:
            author_serializer = AuthorSerializer(book.author)
            data['author'] = author_serializer.data
        if book.publisher:
            publisher_serializer = PublisherSerializer(book.publisher)
            data['publisher'] = publisher_serializer.data

        buyers = book.buyers.all()
        buyer_serializer = BuyerSerializer(buyers, many=True)
        data['buyers'] = buyer_serializer.data

        return Response(data)

    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def books_with_pages_above(request, min_pages):
    books = Book.objects.filter(
        number_of_pages__gte=min_pages)  # filter by number_of_pages greater than or equal to min_pages
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# Author views
@api_view(['GET'])
def authors_list(request):
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def author_create(request):
    serializer = AuthorSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
    except:
        return Response({'error': 'Author does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AuthorSerializer(author)
        data = serializer.data

        books = Book.objects.filter(author=author)
        books_serializer = BookSerializer(books, many=True)
        data['books'] = books_serializer.data

        return Response(data)

    if request.method == 'PUT':
        serializer = AuthorSerializer(author, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        author.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Publisher views
@api_view(['GET'])
def publishers_list(request):
    publishers = Publisher.objects.all()
    serializer = PublisherSerializer(publishers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def publisher_create(request):
    serializer = PublisherSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def publisher_detail(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)
    except:
        return Response({'error': 'Publisher does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PublisherSerializer(publisher)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = PublisherSerializer(publisher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        publisher.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def buyers_list(request):
    buyers = Buyer.objects.all()
    serializer = BuyerSerializer(buyers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def buyer_create(request):
    serializer = BuyerSerializer(data=request.data)
    if serializer.is_valid():
        buyer = serializer.save()

        book_ids = request.data.get('books', [])
        purchases = []
        for book_id in book_ids:
            book = get_object_or_404(Book, id=book_id)
            purchase = Purchase(buyer=buyer, book=book, price=book.price)
            purchases.append(purchase)

        Purchase.objects.bulk_create(purchases)
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


from rest_framework import status


@api_view(['GET', 'PUT', 'DELETE'])
def buyer_detail(request, pk):
    try:
        buyer = Buyer.objects.get(pk=pk)
    except Buyer.DoesNotExist:
        return Response({'error': 'Buyer does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BuyerSerializer(buyer)
        data = serializer.data
        books = Book.objects.filter(purchase__buyer=buyer).distinct()
        book_serializer = BookSerializer(books, many=True)
        data['books'] = book_serializer.data
        return Response(data)

    elif request.method == 'PUT':
        serializer = BuyerSerializer(buyer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        buyer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# BuyerSubscription views
@api_view(['GET'])
def subscriptions_list(request):
    subscriptions = BuyerSubscription.objects.all()
    serializer = BuyerSubscriptionSerializer(subscriptions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def subscription_create(request):
    serializer = BuyerSubscriptionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
def subscription_detail(request, pk):
    try:
        subscription = BuyerSubscription.objects.get(pk=pk)
    except:
        return Response({'error': 'Subscription does not exist!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BuyerSubscriptionSerializer(subscription)
        data = serializer.data

        buyer_serializer = BuyerSerializer(subscription.buyer)
        data['buyer'] = buyer_serializer.data

        return Response(data)

    if request.method == 'PUT':
        serializer = BuyerSubscriptionSerializer(subscription, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def publisher_stats(request):
    # Calculate the average number of pages for books published by each publisher
    publisher_page_stats = (
        Publisher.objects.annotate(average_number_of_pages=Avg('book__number_of_pages'))
        .values('name', 'average_number_of_pages')
        .order_by('name')
    )

    # Create a list of DTO instances
    publisher_stats = [
        PublisherStatsDTO(publisher_name=stat['name'], average_number_of_pages=stat['average_number_of_pages'])
        for stat in publisher_page_stats
    ]

    # Serialize the DTO instances
    serializer = PublisherStatsDTOSerializer(publisher_stats, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data)

@api_view(['GET'])
def author_stats(request):
    # Calculate the average number of pages for books written by each author
    author_page_stats = (
        Author.objects.annotate(average_number_of_pages=Avg('book__number_of_pages'))
        .exclude(average_number_of_pages__isnull=True)
        .values('first_name', 'average_number_of_pages')
        .order_by('first_name')
    )

    # Create a list of DTO instances
    author_stats = [
        AuthorStatsDTO(author_first_name=stat['first_name'], average_number_of_pages=stat['average_number_of_pages'])
        for stat in author_page_stats
    ]

    # Serialize the DTO instances
    serializer = AuthorStatsDTOSerializer(author_stats, many=True)

    # Return the serialized data as a JSON response
    return Response(serializer.data)

# @api_view(['POST'])
# def add_buyer_to_book(request, id):
#     try:
#         book = Book.objects.get(pk=id)
#         buyer_id = request.data.get('buyer_id')
#         buyer = Buyer.objects.get(pk=buyer_id)
#         book.buyers.add(buyer)
#         book.save()
#         return Response({'success': True, 'message': 'Buyer added successfully to the book.'},
#                         status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['DELETE'])
# def remove_buyer_from_book(request, id, buyer_id):
#     try:
#         book = Book.objects.get(pk=id)
#         buyer = Buyer.objects.get(pk=buyer_id)
#         book.buyers.remove(buyer)
#         book.save()
#         return Response({'success': True, 'message': 'Buyer removed successfully from the book.'},
#                         status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response({'success': False, 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def book_add_buyer(request, id):
    book = get_object_or_404(Book, id=id)
    buyer_id = request.data.get('buyer_id')
    buyer = get_object_or_404(Buyer, id=buyer_id)

    book.buyers.add(buyer)
    book.save()

    purchase = Purchase(book=book, buyer=buyer, price=book.price)
    purchase.save()

    return Response({'success': True, 'message': 'Buyer added successfully to the book.'},
                    status=status.HTTP_201_CREATED)


@api_view(['PATCH'])
def book_update_buyers(request, id):
    book = get_object_or_404(Book, id=id)
    buyer_ids = request.data.get('buyer_ids')

    # Clear all the existing buyers
    book.buyers.clear()

    # Delete all the purchases with the specified book ID and buyer ID
    for buyer_id in buyer_ids:
        buyer = get_object_or_404(Buyer, id=buyer_id)
        Purchase.objects.filter(book=book, buyer=buyer).delete()

        # Add the buyer to the book
        book.buyers.add(buyer)

        # Create a new purchase with the updated buyer and book
        purchase = Purchase(book=book, buyer=buyer, price=book.price)
        purchase.save()

    return Response({'success': True, 'message': 'Buyers updated successfully for the book.'},
                    status=status.HTTP_200_OK)

@api_view(['PUT', 'DELETE'])
def book_update_or_delete_buyer(request, id, buyer_id):
    book = get_object_or_404(Book, id=id)
    buyer = get_object_or_404(Buyer, id=buyer_id)

    if request.method == 'PUT':
        new_price = request.data.get('price')

        if new_price:
            purchase = get_object_or_404(Purchase, book=book, buyer=buyer)
            purchase.price = new_price
            purchase.save()
            return Response({'success': True, 'message': 'Purchase updated successfully.'},
                            status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Missing price information.'},
                        status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        purchase = get_object_or_404(Purchase, book=book, buyer=buyer)
        purchase.delete()
        book.buyers.remove(buyer)
        book.save()
        return Response({'success': True, 'message': 'Buyer removed from the book.'},
                        status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def buyer_add_book(request, id):
    buyer = get_object_or_404(Buyer, id=id)
    book_id = request.data.get('book_id')

    if book_id:
        book = get_object_or_404(Book, id=book_id)
        purchase = Purchase(buyer=buyer, book=book, price=book.price)
        purchase.save()
        return Response({'success': True, 'message': 'Book added to the buyer.'},
                        status=status.HTTP_201_CREATED)

    return Response({'success': False, 'message': 'Missing book_id information.'},
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def buyer_update_or_delete_book(request, id, book_id):
    buyer = get_object_or_404(Buyer, id=id)
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'PUT':
        new_price = request.data.get('price')

        if new_price:
            purchase = get_object_or_404(Purchase, book=book, buyer=buyer)
            purchase.price = new_price
            purchase.save()
            return Response({'success': True, 'message': 'Purchase updated successfully.'},
                            status=status.HTTP_200_OK)

        return Response({'success': False, 'message': 'Missing price information.'},
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        purchase = Purchase.objects.filter(book=book, buyer=buyer).first()
        if purchase:
            purchase.delete()
            return Response({'success': True, 'message': 'Book removed from the buyer.'},
                            status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'success': False, 'message': 'No matching purchase found.'},
                            status=status.HTTP_404_NOT_FOUND)
