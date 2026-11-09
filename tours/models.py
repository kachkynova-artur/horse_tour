from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """
    Профиль пользователя.

    Связь один-к-одному (1:1) с моделью User.
    Каждый пользователь может иметь один профиль.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        help_text="Пользователь, которому принадлежит профиль."
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        help_text="Номер телефона пользователя."
    )

    bio = models.TextField(
        blank=True,
        help_text="Дополнительная информация о пользователе."
    )

    def __str__(self):
        return self.user.username


class Category(models.Model):
    """
    Категория туристического маршрута.

    Примеры категорий: Конный, Пеший, Мото.
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Название категории туристического маршрута."
    )

    def __str__(self):
        return self.name


class Tour(models.Model):
    """
    Туристический маршрут.

    Один тур может относиться к нескольким категориям.
    Используется связь многие-ко-многим (M:N) с моделью Category.
    """

    name = models.CharField(
        max_length=200,
        help_text="Название туристического маршрута."
    )

    description = models.TextField(
        help_text="Подробное описание туристического маршрута."
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Стоимость туристического маршрута."
    )

    categories = models.ManyToManyField(
        Category,
        related_name="tours",
        help_text="Категории, к которым относится тур."
    )

    def __str__(self):
        return self.name


class Booking(models.Model):
    """
    Бронирование туристического маршрута.

    Пользователь может забронировать тур на определённую
    дату и время.

    Один пользователь не может забронировать два разных
    тура на одну и ту же дату и время.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="Пользователь, который бронирует тур."
    )

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="bookings",
        help_text="Тур, который бронирует пользователь."
    )

    date = models.DateField(
        help_text="Дата проведения тура."
    )

    time = models.TimeField(
        help_text="Время проведения тура."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания бронирования."
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "date", "time"],
                name="unique_user_booking_datetime"
            )
        ]

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"


class Comment(models.Model):
    """
    Комментарий пользователя к туристическому маршруту.

    Пользователь может оставить несколько комментариев
    к туру, который он бронировал.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Автор комментария."
    )

    tour = models.ForeignKey(
        Tour,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="Тур, к которому относится комментарий."
    )

    text = models.TextField(
        help_text="Текст комментария пользователя."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата и время создания комментария."
    )

    def __str__(self):
        return f"{self.user.username} - {self.tour.name}"