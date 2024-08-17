from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError


from django.db import models

class CustomUser(AbstractUser):
    """Кастомная модель пользователя - студента."""

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=250,
        unique=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
        'password'
    )


    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.get_full_name()


class Balance(models.Model):
    """Модель баланса пользователя."""


    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000,
        verbose_name='Баланс'
    )

    # TODO

    user = models.OneToOneField(
        CustomUser,
        related_name='balance',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def save(self, *args, **kwargs):
        if self.balance < 0:
            raise ValidationError("Баланс не может быть ниже 0.")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
        ordering = ('-id',)


class Subscription(models.Model):
    """Модель подписки пользователя на курс."""

    # TODO

    course = models.ForeignKey(
        'courses.Course',
        related_name='subs',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        CustomUser,
        related_name='sub',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        ordering = ('-id',)
