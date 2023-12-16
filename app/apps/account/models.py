from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Friends(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user"
    )
    friends = models.ManyToManyField(User, blank=True, related_name="friends")

    def __str__(self) -> str:
        return self.user.username

    def add_friend(self, account):  # add friend
        if not account in self.friends.all():
            self.friends.add(account)
            self.save()

    def delete_friend(self, account):  # remove friend
        if account in self.friends.all():
            self.friends.remove(account)

    def is_friends(self, account):
        if account in self.friends.all():
            return True
        return False
