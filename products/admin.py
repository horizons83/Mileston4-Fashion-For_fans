from django.contrib import admin
from .models import Product, Team, Category, Review

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class TeamAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


class ReviewInline(admin.TabularInline):
    """ Allows view/edit of reviews from Product detail page """
    model = Review


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'category',
        'team',
        'size',
        'qty',
        'price',
        'image',
    )

    ordering = ('sku',)

    inlines = [
        ReviewInline,
    ]


class ReviewAdmin(admin.ModelAdmin):
    """ Add product review section in admin dashboard """

    list_display = (
        'review_title',
        'reviewer',
        'product',
        'rating'
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
