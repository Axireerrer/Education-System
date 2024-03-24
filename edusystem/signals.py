from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from edusystem.models import ProductAccess, Group
from edusystem.utils import time_started


@receiver(post_save, sender=ProductAccess)
def create_group(sender, instance, created, **kwargs):
    product = instance.product
    user = instance.user
    groups = Group.objects.filter(product=product).annotate(
        user_count=Count('user')
    ).order_by('user_count')

    if created:
        if time_started() != product.time_start:
            for group in groups:
                if group.user_count < product.max_users_group:
                    group.user.add(user)
                break
        else:
            new_group = Group.objects.create(product=product)
            new_group.user.add(user)
    else:
        smallest_group = groups.first()
        smallest_group.user.add(user)









