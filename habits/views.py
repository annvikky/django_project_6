from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, generics, permissions, viewsets

from .models import Habit
from .permissions import IsOwnerOrReadOnly
from .serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["time"]

    def get_queryset(self):
        if self.action == "list":
            return Habit.objects.filter(user=self.request.user).order_by("id")
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @swagger_auto_schema(
        operation_description="Получить список привычек текущего пользователя",
        responses={200: HabitSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Создать новую привычку. Пользователь устанавливается автоматически.",
        responses={201: HabitSerializer()},
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Получить одну привычку по ID",
        responses={200: HabitSerializer()},
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить привычку целиком (PUT)",
        responses={200: HabitSerializer()},
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Обновить привычку частично (PATCH)",
        responses={200: HabitSerializer()},
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Удалить привычку по ID", responses={204: "No Content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class PublicHabitListView(generics.ListAPIView):
    queryset = Habit.objects.filter(is_public=True).order_by("id")
    serializer_class = HabitSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Получить список публичных привычек (is_public=True)",
        responses={200: HabitSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
