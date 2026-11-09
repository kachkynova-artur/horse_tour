from datetime import date, time

from django.contrib.auth.models import User
from django.db import IntegrityError
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from tours.models import Profile, Category, Tour, Booking, Comment

class ModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ivan",
            password="12345678"
        )

        self.user2 = User.objects.create_user(
            username="anna",
            password="12345678"
        )

        self.category_horse = Category.objects.create(
            name="Конный"
        )

        self.category_walk = Category.objects.create(
            name="Пеший"
        )

        self.category_moto = Category.objects.create(
            name="Мото"
        )

        self.tour = Tour.objects.create(
            name="Конная прогулка",
            description="Прогулка на лошадях",
            price=3000
        )

        self.tour.categories.add(
            self.category_horse,
            self.category_walk
        )

    def test_one_to_one_profile(self):
        profile = Profile.objects.create(
            user=self.user,
            phone="+996700000000",
            bio="Люблю лошадей"
        )

        self.assertEqual(profile.user, self.user)
        self.assertEqual(self.user.profile, profile)

    def test_many_to_many_categories(self):
        self.assertEqual(
            self.tour.categories.count(),
            2
        )

    def test_booking_creation(self):
        booking = Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.tour, self.tour)

    def test_user_cannot_book_two_tours_same_datetime(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        another_tour = Tour.objects.create(
            name="Мото-тур",
            description="Мото прогулка",
            price=5000
        )

        with self.assertRaises(IntegrityError):
            Booking.objects.create(
                user=self.user,
                tour=another_tour,
                date=date(2026, 11, 20),
                time=time(10, 0)
            )

    def test_user_can_book_different_time(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        booking = Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(14, 0)
        )

        self.assertIsNotNone(booking)

    def test_user_can_leave_multiple_comments(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        Comment.objects.create(
            user=self.user,
            tour=self.tour,
            text="Первый комментарий"
        )

        Comment.objects.create(
            user=self.user,
            tour=self.tour,
            text="Второй комментарий"
        )

        self.assertEqual(
            Comment.objects.filter(
                user=self.user,
                tour=self.tour
            ).count(),
            2
        )

        from rest_framework import status
from rest_framework.test import APITestCase

from tours.models import Category, Tour, Booking, Comment


class APITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="ivan",
            password="12345678"
        )

        self.user2 = User.objects.create_user(
            username="anna",
            password="12345678"
        )

        self.category_horse = Category.objects.create(
            name="Конный"
        )

        self.category_walk = Category.objects.create(
            name="Пеший"
        )

        self.tour = Tour.objects.create(
            name="Конная прогулка",
            description="Прогулка на лошадях",
            price=3000
        )

        self.tour.categories.add(
            self.category_horse,
            self.category_walk
        )

    def test_get_tours(self):
        response = self.client.get("/api/tours/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(response.data), 1)

    def test_create_category(self):
        response = self.client.post(
            "/api/categories/",
            {
                "name": "Мото"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_create_tour_with_categories(self):
        response = self.client.post(
            "/api/tours/",
            {
                "name": "Экстремальный тур",
                "description": "Горный туристический маршрут",
                "price": "5000.00",
                "categories": [
                    self.category_horse.id,
                    self.category_walk.id
                ]
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            len(response.data["categories"]),
            2
        )

    def test_create_booking(self):
        response = self.client.post(
            "/api/bookings/",
            {
                "user": self.user.id,
                "tour": self.tour.id,
                "date": "2026-11-20",
                "time": "10:00:00"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_duplicate_booking_same_datetime(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        another_tour = Tour.objects.create(
            name="Мото-тур",
            description="Мото прогулка",
            price=5000
        )

        response = self.client.post(
            "/api/bookings/",
            {
                "user": self.user.id,
                "tour": another_tour.id,
                "date": "2026-11-20",
                "time": "10:00:00"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_booking_different_time_is_allowed(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        response = self.client.post(
            "/api/bookings/",
            {
                "user": self.user.id,
                "tour": self.tour.id,
                "date": "2026-11-20",
                "time": "14:00:00"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_comment_without_booking_is_forbidden(self):
        response = self.client.post(
            "/api/comments/",
            {
                "user": self.user.id,
                "tour": self.tour.id,
                "text": "Отличный тур!"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_comment_after_booking(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        response = self.client.post(
            "/api/comments/",
            {
                "user": self.user.id,
                "tour": self.tour.id,
                "text": "Мне очень понравилось!"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_can_leave_multiple_comments(self):
        Booking.objects.create(
            user=self.user,
            tour=self.tour,
            date=date(2026, 11, 20),
            time=time(10, 0)
        )

        response1 = self.client.post(
            "/api/comments/",
            {
                "user": self.user.id,
                "tour": self.tour.id,
                "text": "Первый комментарий"
            },
            format="json"
        )

        response2 = self.client.post(
            "/api/comments/",
            {
                "user": self.user.id,
                "tour": self.tour.id,
                "text": "Второй комментарий"
            },
            format="json"
        )

        self.assertEqual(
            response1.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response2.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Comment.objects.filter(
                user=self.user,
                tour=self.tour
            ).count(),
            2
        )