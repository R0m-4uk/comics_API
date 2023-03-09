from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserView, ComicsView, ComicsDetailView, AuthorDetailView, CartView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),

    path('user/', UserView.as_view({'get': 'get_user'})),

    path('comics/', ComicsView.as_view({'get': 'get_comics_list'})),
    path('comics/<int:pk>/', ComicsDetailView.as_view({'get': 'get_comics'})),

    path('author/<int:pk>/', AuthorDetailView.as_view({'get': 'get_author'})),

    path('cart/', CartView.as_view({'get': 'get_cart'})),
    path('cart/add/', CartView.as_view({'post': 'add_in_cart'})),
    path('cart/update/', CartView.as_view({'put': 'update_count_comics'})),
    path('cart/pop/', CartView.as_view({'delete': 'pop_cart'})),
]
