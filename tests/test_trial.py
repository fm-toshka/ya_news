# # news/tests/test_trial.py
# import unittest  # импорт  unittest из стд библиотеки
# from django.test import TestCase, Client
# from django.contrib.auth import get_user_model
# from news.models import News

# User = get_user_model()

# @unittest.skip()
# class TestNews(TestCase):
#     # Все нужные переменные сохраняем в атрибуты класса.
#     TITLE = 'Заголовок новости'
#     TEXT = 'Тестовый текст'
    
#     @classmethod
#     def setUpTestData(cls):
#         cls.news = News.objects.create(
#             # При создании объекта обращаемся к константам класса через cls.
#             title=cls.TITLE,
#             text=cls.TEXT,
#         )
#         # Создаём пользователя.
#         cls.user = User.objects.create(username='testUser')
#         # Создаём объект клиента.
#         cls.user_client = Client()
#         # "Логинимся" в клиенте при помощи метода force_login().        
#         cls.user_client.force_login(cls.user)
#         # Теперь через этот клиент можно отправлять запросы
#         # от имени пользователя с логином "testUser". 

#     def test_successful_creation(self):
#         news_count = News.objects.count()
#         self.assertEqual(news_count, 1)

#     def test_title(self):
#         # Чтобы проверить равенство с константой -
#         # обращаемся к ней через self, а не через cls:
#         self.assertEqual(self.news.title, self.TITLE)

        
# # from django.test import TestCase


# # class Test(TestCase):

# #     def test_example_success(self):
# #         self.assertTrue(True)  # Этот тест всегда будет проходить успешно.


# # class YetAnotherTest(TestCase):

# #     def test_example_fails(self):
# #         self.assertTrue(False)  # Этот тест всегда будет проваливаться.