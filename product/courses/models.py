from django.core.exceptions import ValidationError
from django.db import models

from users.models import CustomUser, Subscription


class Course(models.Model):
    """Модель продукта - курса."""

    # author = models.CharField(
    #     max_length=250,
    #     verbose_name='Автор',
    # )



    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Стоимость'
    )

    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )

    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )

    available_flag = models.BooleanField(default=True)

    # TODO

    author = models.ForeignKey(
        CustomUser,
        related_name='courses_created',
        on_delete=models.CASCADE
    )

    students = models.ManyToManyField(
        CustomUser,
        related_name='courses_joined',
        blank=True,
        through=Subscription
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""


    title = models.CharField(
        max_length=250,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=250,
        verbose_name='Ссылка',
    )

    # TODO

    course = models.ForeignKey(
        Course,
        related_name='lessons',
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title




class Group(models.Model):
    """Модель группы."""

    # TODO

    course = models.ForeignKey(
        Course,
        related_name='groups',
        on_delete=models.CASCADE,
        null=False
    )

    users = models.ManyToManyField(
        CustomUser,
        blank=True
    )




    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)
