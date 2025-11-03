from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import User
from apps.habits.models import Habit


class HabitApiTests(APITestCase):

    def setUp(self):
        # Создаем двух пользователей с УНИКАЛЬНЫМИ username
        self.user1 = User.objects.create_user(
            username='user1_unique',  # <-- Изменено
            email='user1@example.com',
            password='password123',
            telegram_id='12345'
        )
        self.user2 = User.objects.create_user(
            username='user2_unique',  # <-- Изменено
            email='user2@example.com',
            password='password123'
        )
        # Аутентифицируем user1
        self.client.login(email='user1@example.com', password='password123')
        # Для APITestCase с JWT, вам нужно получить токен и установить его в заголовок
        # Но для простоты в тестах можно использовать force_authenticate
        self.client.force_authenticate(user=self.user1)

        # Создаем приятную привычку для user1
        self.pleasant_habit = Habit.objects.create(
            user=self.user1,
            place='Дом',
            time='21:00:00',
            action='Принять ванну',
            is_pleasant=True,
            periodicity=1,
            duration=100
        )

        # Создаем полезную привычку (публичную) для user2
        self.public_habit_user2 = Habit.objects.create(
            user=self.user2,
            place='Парк',
            time='08:00:00',
            action='Пробежка',
            reward='Съесть фрукт',
            periodicity=1,
            duration=120,
            is_public=True
        )

    def test_create_habit_with_reward(self):
        """Тест создания полезной привычки с вознаграждением."""
        url = reverse('habits:habit-list')
        data = {
            "place": "Офис",
            "time": "14:00:00",
            "action": "Сделать зарядку для глаз",
            "reward": "Выпить чашку чая",
            "periodicity": 1,
            "duration": 60,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)
        self.assertEqual(response.data['action'], 'Сделать зарядку для глаз')
        self.assertEqual(response.data['reward'], 'Выпить чашку чая')

    def test_create_habit_with_related_habit(self):
        """Тест создания полезной привычки со связанной приятной."""
        url = reverse('habits:habit-list')
        data = {
            "place": "Дом",
            "time": "20:30:00",
            "action": "Почитать книгу 15 минут",
            "related_habit": self.pleasant_habit.id,
            "periodicity": 1,
            "duration": 120,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['action'], 'Почитать книгу 15 минут')

    # --- Тесты валидаторов ---

    def test_fail_create_habit_with_both_reward_and_related(self):
        """(Валидатор 1) Ошибка: одновременное вознаграждение и связанная привычка."""
        url = reverse('habits:habit-list')
        data = {
            "place": "Место",
            "time": "10:00:00",
            "action": "Действие",
            "reward": "Награда",
            "related_habit": self.pleasant_habit.id,
            "periodicity": 1,
            "duration": 60,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Нельзя одновременно', str(response.data))

    def test_fail_create_habit_duration_too_long(self):
        """(Валидатор 2) Ошибка: время выполнения > 120 секунд."""
        data = {
            "place": "Место", "time": "10:00:00", "action": "Действие",
            "reward": "Награда", "periodicity": 1, "duration": 121,
        }
        response = self.client.post(reverse('habits:habit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('120 секунд', str(response.data))

    def test_fail_create_habit_related_not_pleasant(self):
        """(Валидатор 3) Ошибка: связанная привычка не является приятной."""
        # Создаем полезную привычку, чтобы на нее сослаться
        not_pleasant = Habit.objects.create(
            user=self.user1, place="Место", time="11:00", action="Полезная",
            reward="Награда", periodicity=1, duration=60, is_pleasant=False
        )
        data = {
            "place": "Место2", "time": "12:00", "action": "Действие2",
            "related_habit": not_pleasant.id, "periodicity": 1, "duration": 60,
        }
        response = self.client.post(reverse('habits:habit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('признаком "приятной"', str(response.data))

    def test_fail_create_pleasant_habit_with_reward(self):
        """(Валидатор 4) Ошибка: у приятной привычки есть вознаграждение."""
        data = {
            "place": "Место", "time": "10:00", "action": "Действие",
            "is_pleasant": True, "reward": "Награда", "periodicity": 1, "duration": 60,
        }
        response = self.client.post(reverse('habits:habit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('У приятной привычки не может быть', str(response.data))

    def test_fail_create_habit_periodicity_too_long(self):
        """(Валидатор 5) Ошибка: периодичность > 7 дней."""
        data = {
            "place": "Место", "time": "10:00", "action": "Действие",
            "reward": "Награда", "periodicity": 8, "duration": 60,
        }
        response = self.client.post(reverse('habits:habit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('не более 7', str(response.data))

    def test_fail_create_useful_habit_without_reward(self):
        """(Валидатор 6) Ошибка: у полезной привычки нет ни награды, ни связанной."""
        data = {
            "place": "Место", "time": "10:00", "action": "Действие",
            "is_pleasant": False, "periodicity": 1, "duration": 60,
        }
        response = self.client.post(reverse('habits:habit-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('У полезной привычки должно быть', str(response.data))

    # --- Тесты прав доступа и эндпоинтов ---

    def test_list_my_habits(self):
        """Тест: пользователь видит только свои привычки в /habits/."""
        url = reverse('habits:habit-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.pleasant_habit принадлежит user1
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.pleasant_habit.id)

    def test_list_public_habits(self):
        """Тест: пользователь видит публичные привычки в /habits/public/."""
        url = reverse('habits:habit-public-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.public_habit_user2 принадлежит user2, но она публичная
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['id'], self.public_habit_user2.id)

    def test_user_cannot_update_other_user_habit(self):
        """Тест: (IsOwner) пользователь не может обновить чужую привычку."""
        url = reverse('habits:habit-detail', kwargs={'pk': self.public_habit_user2.id})
        data = {"place": "Новое место"}
        response = self.client.patch(url, data, format='json')

        # public_habit_user2 принадлежит user2, а мы аутентифицированы как user1
        self.assertEqual(response.status_code,
                         status.HTTP_404_NOT_FOUND)  # ViewSet вернет 404, т.к. get_queryset ее не найдет

    def test_user_can_update_own_habit(self):
        """Тест: (IsOwner) пользователь может обновить свою привычку."""
        url = reverse('habits:habit-detail', kwargs={'pk': self.pleasant_habit.id})
        data = {"place": "Ванная комната"}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.pleasant_habit.refresh_from_db()
        self.assertEqual(self.pleasant_habit.place, "Ванная комната")
