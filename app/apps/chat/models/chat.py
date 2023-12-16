from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from .managers import ThreadManager

User = get_user_model()


class TrackingModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]


class Chat(TrackingModel):
    class ThreadType(models.TextChoices):
        personal = ("personal", "Personal")
        group = ("group", "Group")

    name = models.CharField(max_length=50, null=True, blank=True)
    chat_type = models.CharField(
        max_length=15, choices=ThreadType.choices, default=ThreadType.group
    )
    thread_id = models.CharField("Chat uniquw Thread ID", max_length=64)

    objects = ThreadManager()

    def __str__(self) -> str:
        if self.chat_type == "personal":
            return f"chat thread: {self.thread_id}"
        return f"{self.name}"


class Group(TrackingModel):
    name = models.CharField(max_length=256)
    users = models.ManyToManyField(User, blank=True, related_name="users")
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, blank=True)

    def add_user(self, account):  # add user to group
        if not account in self.users.all():
            self.friends.add(account)
            self.save()

    def remove_user(self, account):  # remove friend
        if account in self.users.all():
            self.friends.remove(account)

    def is_friends(self, account):
        if account in self.users.all():
            return True
        return False


class Message(TrackingModel):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ["created_at"]

    def __str__(self):
        return str(self.id) + " " + "content: " + self.content


class UserMessage(Message):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_from_me"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="messages_to_me"
    )

    class Meta:
        ordering = ("-timestamp",)


class GroupMessage(Message):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    class Meta:
        ordering = ("-timestamp",)
