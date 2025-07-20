from rest_framework import serializers


def validate_no_reward_and_related_habit(reward, related_habit):
    if reward and related_habit:
        raise serializers.ValidationError(
            "Нельзя одновременно указывать и вознаграждение, и связанную привычку."
        )


def validate_pleasant_has_no_reward_or_related(is_pleasant, reward, related_habit):
    if is_pleasant and (reward or related_habit):
        raise serializers.ValidationError(
            "У приятной привычки не может быть ни вознаграждения, ни связанной привычки."
        )


def validate_related_habit_is_pleasant(related_habit):
    if related_habit and not related_habit.is_pleasant:
        raise serializers.ValidationError("Можно связать только с приятной привычкой.")


def validate_duration(duration):
    if duration > 120:
        raise serializers.ValidationError(
            "Время выполнения не может превышать 120 секунд."
        )


def validate_periodicity(periodicity):
    if periodicity < 1 or periodicity > 7:
        raise serializers.ValidationError("Периодичность должна быть от 1 до 7 дней.")
