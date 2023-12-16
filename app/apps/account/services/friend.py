from django.db import transaction

from apps.account.models import Friends


@transaction.atomic
def create_friends_obj(user):
    firends_obj = Friends(user=user)
    firends_obj.save()
    return firends_obj
