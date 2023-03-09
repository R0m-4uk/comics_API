from django.contrib import admin

from .models import Format, AgeLimit, Available, Comics, Post, Author, ComicsAuthor, Delivery, ComicsDelivery, Cart


class FormatAdmin(admin.ModelAdmin):
    pass


class AgeLimitAdmin(admin.ModelAdmin):
    pass


class AvailableAdmin(admin.ModelAdmin):
    pass


class ComicsAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class ComicsAuthorAdmin(admin.ModelAdmin):
    pass


class DeliveryAdmin(admin.ModelAdmin):
    pass


class ComicsDeliveryAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    pass


admin.site.register(Format, FormatAdmin)
admin.site.register(AgeLimit, AgeLimitAdmin)
admin.site.register(Available, AvailableAdmin)
admin.site.register(Comics, ComicsAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(ComicsAuthor, ComicsAuthorAdmin)
admin.site.register(Delivery, DeliveryAdmin)
admin.site.register(ComicsDelivery, ComicsDeliveryAdmin)
admin.site.register(Cart, CartAdmin)
