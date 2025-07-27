from rest_framework import serializers

from .models import Habit
from .validators import (validate_duration, validate_no_reward_and_related_habit, validate_periodicity,
                         validate_pleasant_has_no_reward_or_related, validate_related_habit_is_pleasant)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user", "created_at")
        extra_kwargs = {
            "place": {"help_text": "Место выполнения действия"},
            "time": {"help_text": "Время выполнения действия"},
            "action": {"help_text": "Описание действия"},
            "is_pleasant": {"help_text": "Является ли привычка приятной"},
            "related_habit": {"help_text": "Связанная приятная привычка"},
            "reward": {"help_text": "Вознаграждение за выполнение привычки"},
            "periodicity": {"help_text": "Периодичность выполнения (в днях)"},
            "duration": {"help_text": "Продолжительность действия в секундах (до 120)"},
            "is_public": {"help_text": "Публичная ли привычка"},
        }

    def validate(self, data):
        validate_no_reward_and_related_habit(
            data.get("reward"), data.get("related_habit")
        )
        validate_pleasant_has_no_reward_or_related(
            data.get("is_pleasant"), data.get("reward"), data.get("related_habit")
        )
        validate_related_habit_is_pleasant(data.get("related_habit"))
        validate_duration(data.get("duration"))
        validate_periodicity(data.get("periodicity"))
        return data
