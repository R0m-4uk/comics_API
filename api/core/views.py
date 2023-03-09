from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comics, Author, Cart
from .serializers import ComicsSerializer, ComicsDetailSerializer, AuthorDetailSerializer, CartSerializer, \
    UserSerializer


class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def get_user(self, request):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComicsView(viewsets.ModelViewSet):
    queryset = Comics.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ComicsSerializer

    @action(methods=['get'], detail=False)
    def get_comics_list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComicsDetailView(viewsets.ModelViewSet):
    queryset = Comics.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ComicsDetailSerializer

    @action(methods=['get'], detail=False)
    def get_comics(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        if not queryset:
            return Response({
                "error": "Такого комикса не существует",
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset[0])
        return Response(serializer.data, status=status.HTTP_200_OK)


class AuthorDetailView(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = AuthorDetailSerializer

    @action(methods=['get'], detail=False)
    def get_author(self, request, pk):
        queryset = self.queryset.filter(pk=pk)
        if not queryset:
            return Response({
                "error": "Такого автора не существует",
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(queryset[0])
        return Response(serializer.data, status=status.HTTP_200_OK)


class CartView(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer

    @action(methods=['get'], detail=False)
    def get_cart(self, request):
        queryset = self.queryset.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def add_in_cart(self, request):
        queryset = Comics.objects.filter(pk=request.data.get('comics'))
        if not queryset:
            return Response({
                "error": "Такого комикса не существует",
            }, status=status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user,
            'comics': queryset[0]
        }
        if self.queryset.filter(**data):
            return Response({
                "error": "Пользователь уже добавил комикс",
            }, status=status.HTTP_404_NOT_FOUND)


        serializer = self.serializer_class(data=request.data, context=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.data)
        return Response({
            'pk': serializer.data['pk'],
            'title': serializer.data['title'],
            'message': "Комикс добавлен в корзину",
        }, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def add_in_cart(self, request):
        queryset = Comics.objects.filter(pk=request.data.get('comics'))
        if not queryset:
            return Response({
                "error": "Такого комикса не существует",
            }, status=status.HTTP_404_NOT_FOUND)
        data = {
            'user': request.user,
            'comics': queryset[0]
        }
        if self.queryset.filter(**data):
            return Response({
                "error": "Пользователь уже добавил комикс",
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data, context=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'pk': serializer.data['pk'],
            'title': serializer.data['comics']['title'],
            'message': "Комикс добавлен в корзину",
        }, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=False)
    def update_count_comics(self, request):
        queryset = Comics.objects.filter(pk=request.data.get('comics'))
        if not queryset:
            return Response({
                "error": "Такого комикса не существует",
            }, status=status.HTTP_404_NOT_FOUND)

        data = self.queryset.filter(user=request.user, comics=queryset[0])
        if not data:
            return Response({
                "error": "Такого комикса нет в корзине",
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data, instance=data[0])
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'pk': serializer.data['pk'],
            'title': serializer.data['comics']['title'],
            'message': "Количество комиксов обновлено в корзине",
        }, status=status.HTTP_200_OK)


    @action(methods=['delete'], detail=False)
    def pop_cart(self, request):
        queryset = Comics.objects.filter(pk=request.data.get('comics'))
        if not queryset:
            return Response({
                "error": "Такого комикса не существует",
            }, status=status.HTTP_404_NOT_FOUND)
        data = self.queryset.filter(user=request.user, comics=queryset[0])
        if not data:
            return Response({
                "error": "Такого комикса нет в корзине",
            }, status=status.HTTP_400_BAD_REQUEST)
        data.delete()

        return Response({
            'pk': queryset[0].pk,
            'title': queryset[0].title,
            'message': "Комикс убран из корзины",
        }, status=status.HTTP_200_OK)


