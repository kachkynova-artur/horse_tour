from django.contrib import admin

from .models import Profile, Category, Tour, Booking, Comment


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price")
    search_fields = ("name",)
    filter_horizontal = ("categories",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tour", "date", "time", "created_at")
    list_filter = ("date", "tour")
    search_fields = ("user__username", "tour__name")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "tour", "created_at")
    search_fields = ("user__username", "tour__name", "text")