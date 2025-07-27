from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Habit

User = get_user_model()


class HabitAPITests(APITestCase):

    def setUp(self):
        """Создание двух пользователей и двух привычек (одна публичная, одна приватная)."""
        self.user1 = User.objects.create_user(
            email="user1@example.com", username="user1", password="pass1234"
        )
        self.user2 = User.objects.create_user(
            email="user2@example.com", username="user2", password="pass1234"
        )

        self.habit1 = Habit.objects.create(
            user=self.user1,
            place="Дом",
            time="09:00:00",
            action="Читать книгу",
            is_pleasant=False,
            periodicity=3,
            duration=60,
            is_public=False,
        )
        self.public_habit = Habit.objects.create(
            user=self.user2,
            place="Парк",
            time="08:00:00",
            action="Медитация",
            is_pleasant=True,
            periodicity=1,
            duration=60,
            is_public=True,
        )

    def get_jwt_token(self, email, password):
        """Получение JWT-токена по email и паролю."""
        url = reverse("users:token_obtain_pair")
        response = self.client.post(url, {"email": email, "password": password})
        return response.data["access"]

    def auth(self, email, password):
        """Аутентификация пользователя через JWT."""
        token = self.get_jwt_token(email, password)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)

    def test_list_habits_authenticated_user_sees_own(self):
        """Авторизованный пользователь видит только свои привычки."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits = response.data.get("results", response.data)
        self.assertEqual(len(habits), 1)
        self.assertEqual(habits[0]["id"], self.habit1.id)

    def test_create_habit(self):
        """Пользователь может создать свою привычку."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:habit-list")
        data = {
            "place": "Офис",
            "time": "10:30:00",
            "action": "Планирование дня",
            "is_pleasant": False,
            "periodicity": 2,
            "duration": 30,
            "is_public": False,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["place"], "Офис")
        self.assertEqual(response.data["user"], self.user1.id)

    def test_retrieve_habit_owner(self):
        """Пользователь может получить свою привычку по id."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:habit-detail", args=[self.habit1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.habit1.id)

    def test_update_habit_owner(self):
        """Пользователь может обновить свою привычку."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:habit-detail", args=[self.habit1.id])
        data = {
            "place": "Библиотека",
            "time": "11:00:00",
            "action": "Читать книгу",
            "is_pleasant": False,
            "periodicity": 3,
            "duration": 45,
            "is_public": True,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["place"], "Библиотека")
        self.assertEqual(response.data["is_public"], True)

    def test_delete_habit_owner(self):
        """Пользователь может удалить свою привычку."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:habit-detail", args=[self.habit1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Habit.objects.filter(id=self.habit1.id).exists())

    def test_cannot_access_other_users_private_habit(self):
        """Пользователь не может получить доступ к чужой приватной привычке."""
        self.auth("user1@example.com", "pass1234")
        private_habit = Habit.objects.create(
            user=self.user2,
            place="Кафе",
            time="15:00:00",
            action="Писать заметки",
            is_pleasant=False,
            periodicity=2,
            duration=40,
            is_public=False,
        )
        url_private = reverse("habits:habit-detail", args=[private_habit.id])
        response_private = self.client.get(url_private)
        self.assertEqual(response_private.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_public_habits_any_user(self):
        """Любой пользователь может просматривать список публичных привычек."""
        url = reverse("habits:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits = response.data.get("results", response.data)
        self.assertTrue(any(h["id"] == self.public_habit.id for h in habits))

    def test_authenticated_user_can_see_public_habits(self):
        """Авторизованный пользователь может просматривать публичные привычки."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:public-habits")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habits = response.data.get("results", response.data)
        self.assertTrue(any(h["id"] == self.public_habit.id for h in habits))

    def test_cannot_modify_or_delete_public_habit_of_other_user(self):
        """Пользователь не может редактировать или удалять публичную привычку другого пользователя."""
        self.auth("user1@example.com", "pass1234")
        url = reverse("habits:habit-detail", args=[self.public_habit.id])

        # Попытка изменить
        update_data = {
            "place": "Пляж",
            "time": "06:00:00",
            "action": "Бег",
            "is_pleasant": True,
            "periodicity": 1,
            "duration": 30,
            "is_public": True,
        }
        response_put = self.client.put(url, update_data)
        self.assertEqual(response_put.status_code, status.HTTP_403_FORBIDDEN)

        # Попытка удалить
        response_delete = self.client.delete(url)
        self.assertEqual(response_delete.status_code, status.HTTP_403_FORBIDDEN)
