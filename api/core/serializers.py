from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Comics, AgeLimit, Format, Available, Post, ComicsAuthor, Author, ComicsDelivery, Cart


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username', 'email')


class ComicsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comics
        fields = ('pk', 'image', 'title', 'price')


class ComicsDetailSerializer(serializers.ModelSerializer):
    format = serializers.SlugRelatedField(slug_field="title", queryset=Format.objects.all())
    age_limit = serializers.SlugRelatedField(slug_field="title", queryset=AgeLimit.objects.all())
    available = serializers.SlugRelatedField(slug_field="title", queryset=Available.objects.all())
    author_list = serializers.SerializerMethodField()
    delivery_list = serializers.SerializerMethodField()

    class Meta:
        model = Comics
        fields = '__all__'

    def get_author_list(self, model):
        queryset = []
        for el in ComicsAuthor.objects.filter(comics=model):
            queryset.append(AuthorSerializer(el.author).data)
        return queryset

    def get_delivery_list(self, model):
        queryset = []
        for el in ComicsDelivery.objects.filter(comics=model):
            queryset.append(el.delivery.title)
        return queryset


class AuthorSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field="title", queryset=Post.objects.all())

    class Meta:
        model = Author
        fields = ('username', 'image', 'post')


class AuthorDetailSerializer(serializers.ModelSerializer):
    post = serializers.SlugRelatedField(slug_field="title", queryset=Post.objects.all())
    comics_list = serializers.SerializerMethodField()

    class Meta:
        model = Author
        fields = '__all__'

    def get_comics_list(self, model):
        queryset = []
        for el in ComicsAuthor.objects.filter(author=model):
            queryset.append(ComicsSerializer(el.comics).data)
        return queryset


class CartSerializer(serializers.ModelSerializer):
    comics = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ('pk', 'comics', 'count')

    def get_comics(self, model):
        return ComicsSerializer(model.comics).data

    def update(self, instance, validated_data):
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        return instance
