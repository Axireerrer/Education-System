from django.contrib.auth.models import AbstractUser
from django.db import models


class Role:
    STUDENT = 'Student'
    TEACHER = 'Teacher'
    choices = [
        (STUDENT, 'Студент'),
        (TEACHER, 'Преподаватель'),
    ]


class User(AbstractUser):
    role = models.CharField('Роль', max_length=20, choices=Role.choices, default=Role.STUDENT)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.first_name


class Product(models.Model):
    title = models.CharField('Название продукта', max_length=30)
    cost = models.PositiveIntegerField('Цена', default=0)
    time_start = models.DateTimeField('Старт продукта')
    time_end = models.DateTimeField('Конец продукта', blank=True, null=True)
    min_users_group = models.PositiveIntegerField('Минимальное кол-во пользователей в группе')
    max_users_group = models.PositiveIntegerField('Максимальное кол-во пользователей в группе')

    objects = models.Manager()

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.min_users_group > self.max_users_group:
            raise ValueError("it is not possible min more than max")
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Продукты'
        verbose_name_plural = 'Продукт'


class Lesson(models.Model):
    title = models.CharField('Название урока', max_length=30)
    link = models.URLField('Ссылка на видео')
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, null=True, related_name='lessons')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class ProductAccess(models.Model):
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, null=True, related_name='accesses')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    is_valid = models.BooleanField('Валидноcть', default=True)

    objects = models.Manager()

    class Meta:
        verbose_name = 'Доступ к продукту'
        verbose_name_plural = 'Доступы к продуктам'

    def __str__(self):
        return f"Права на доступ к {self.product} пользователя: {self.user}"


class Group(models.Model):
    title = models.CharField('Название группы', max_length=30)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING, related_name='groups', null=True)
    user = models.ManyToManyField('User', related_name='groups_user')

    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

