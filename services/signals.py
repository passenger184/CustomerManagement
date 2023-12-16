from django.db.models.signals import post_save
from django.contrib.auth.models import User, Group
from .models import Custmor


def customer_profile(sender, instance, created, **kwargs):
    if created:
        group = Group.objects.get(name='customer')
        instance.groups.add(group)
        
        Custmor.objects.create(  #assigning customer automatically to user
                user=instance,
                name=instance.username,
            )

post_save.connect(customer_profile, sender=User)            