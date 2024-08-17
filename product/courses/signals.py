import requests
from django.contrib.auth.middleware import get_user
from django.db.models import Count, Min
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from courses.models import Group
from users.models import Subscription


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.

    """

    if created:
        # TODO
        user = instance.user
        g = Group.objects.filter(course=instance.course).annotate(
            members_count=Count('users')
        ).order_by('members_count').first()
        g.users.add(user)
        g.save()



