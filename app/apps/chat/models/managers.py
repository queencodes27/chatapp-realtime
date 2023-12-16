from django.db import models
from django.db.models import Count


class ThreadManager(models.Manager):
    def get_or_create_personal_thread(self, user1, user2):
        users_hash = str(hash(tuple(sorted([user1.id, user2.id]))))
        threads = (
            self.get_queryset()
            .filter(chat_type="personal")
            .filter(thread_id=users_hash)
        )

        if threads.exists():
            return threads.first()
        else:
            thread = self.create(
                name=f"chat_{users_hash}",
                chat_type="personal",
                thread_id=users_hash,
            )
            return thread

    def get_or_create_group_thread(self, group_name):
        group_hash = str(hash(group_name))
        threads = (
            self.get_queryset()
            .filter(chat_type="group")
            .filter(thread_id=group_hash)
        )

        if threads.exists():
            return threads.first()
        else:
            thread = self.create(
                name=f"chat_{group_hash}",
                chat_type="group",
                thread_id=group_hash,
            )
            return thread
