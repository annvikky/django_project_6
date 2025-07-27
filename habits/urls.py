from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.apps import UsersConfig

from .views import HabitViewSet, PublicHabitListView

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habit")

urlpatterns = [
    path("habits/public/", PublicHabitListView.as_view(), name="public-habits"),
    path("", include(router.urls)),
]
