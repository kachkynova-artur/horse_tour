from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    ProfileViewSet,
    CategoryViewSet,
    TourViewSet,
    BookingViewSet,
    CommentViewSet,
)


router = DefaultRouter()

router.register("users", UserViewSet)
router.register("profiles", ProfileViewSet)
router.register("categories", CategoryViewSet)
router.register("tours", TourViewSet)
router.register("bookings", BookingViewSet)
router.register("comments", CommentViewSet)

urlpatterns = router.urls