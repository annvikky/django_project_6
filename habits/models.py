from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits"
    )

    place = models.CharField(max_length=255, help_text="Место выполнения действия")
    time = models.TimeField(help_text="Время выполнения действия")
    action = models.CharField(max_length=255, help_text="Описание действия")

    is_pleasant = models.BooleanField(default=False, help_text="Приятная привычка")

    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={"is_pleasant": True},
        related_name="linked_to",
        help_text="Связанная привычка",
    )

    reward = models.CharField(
        max_length=255, blank=True, null=True, help_text="Вознаграждение"
    )

    periodicity = models.PositiveSmallIntegerField(
        default=1, help_text="Периодичность выполнения в днях (не реже 1 раза в 7 дней)"
    )

    duration = models.PositiveSmallIntegerField(
        help_text="Время выполнения в секундах (максимум 120 секунд)"
    )

    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} в {self.time} в {self.place}"
