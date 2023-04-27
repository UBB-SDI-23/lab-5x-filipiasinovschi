from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from rest_framework import permissions

from .views import (
    books_list,
    book_create,
    book_detail,
    authors_list,
    author_create,
    author_detail,
    publishers_list,
    publisher_create,
    publisher_detail,
    books_with_pages_above,
    buyers_list,
    buyer_create,
    buyer_detail,
    subscriptions_list,
    subscription_create,
    subscription_detail,
    publisher_stats,
    book_add_buyer,
    book_update_or_delete_buyer,
    buyer_add_book,
    buyer_update_or_delete_book,
    book_update_buyers, author_stats
)

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="BOOKS API",
        default_version="1.0.0",
        description="API documentation"
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('books/list/', books_list),
    path('books/', book_create),
    path('books/<int:pk>/', book_detail),
    path('authors/list/', authors_list),
    path('authors/', author_create),
    path('authors/<int:pk>/', author_detail),
    path('publishers/list/', publishers_list),
    path('publishers/', publisher_create),
    path('publishers/<int:pk>/', publisher_detail),
    path('books/above/<int:min_pages>/', books_with_pages_above, name='books_with_pages_above'),
    path('buyers/list/', buyers_list),
    path('buyers/', buyer_create),
    path('buyers/<int:pk>/', buyer_detail),
    path('subscriptions/list/', subscriptions_list),
    path('subscriptions/', subscription_create),
    path('subscriptions/<int:pk>/', subscription_detail),
    path('publisher_stats/', publisher_stats, name='publisher_stats'),
    path('author_stats/', author_stats, name='author_stats'),
    path('books/<int:id>/buyers/', book_add_buyer, name='book-add-buyer'),
    path('books/<int:id>/buyers/<int:buyer_id>/', book_update_or_delete_buyer, name='book-update-or-delete-buyer'),
    path('buyers/<int:id>/books/', buyer_add_book, name='buyer-add-book'),
    path('buyers/<int:id>/books/<int:book_id>/', buyer_update_or_delete_book, name='buyer-update-or-delete-book'),
    path('books/<int:id>/buyers/update', book_update_buyers),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema')
]
