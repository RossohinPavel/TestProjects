from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from users.models import Subscription
from courses.models import Group


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """
    Распределение нового студента в группу курса.
    
    """
    if created:
        group = (
            Group.objects
            .filter(course=instance.course)
            .annotate(user_count=Count('users'))
            .order_by('user_count')
            .first()
        )
        group.users.add(instance.user)
        group.save()
