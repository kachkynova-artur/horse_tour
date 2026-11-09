from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Category, Tour, Booking, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user", "phone", "bio"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class TourSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Tour
        fields = [
            "id",
            "name",
            "description",
            "price",
            "categories",
        ]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "tour",
            "date",
            "time",
            "created_at",
        ]

    def validate(self, data):
        user = data["user"]
        date = data["date"]
        time = data["time"]

        exists = Booking.objects.filter(
            user=user,
            date=date,
            time=time
        ).exists()

        if exists:
            raise serializers.ValidationError(
                "Этот пользователь уже забронировал тур "
                "на указанную дату и время."
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "user",
            "tour",
            "text",
            "created_at",
        ]

    def validate(self, data):
        user = data["user"]
        tour = data["tour"]

        booking_exists = Booking.objects.filter(
            user=user,
            tour=tour
        ).exists()

        if not booking_exists:
            raise serializers.ValidationError(
                "Пользователь не может оставить комментарий "
                "к туру, который он не бронировал."
            )

        return data