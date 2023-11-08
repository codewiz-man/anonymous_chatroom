# chat/cron.py

from django_cron import CronJobBase, Schedule
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class CleanupInactiveUsersCronJob(CronJobBase):
    RUN_EVERY_MINS = 1  # Run the cron job every 60 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'chat.cleanup_inactive_users_cron_job'

    def do(self):
        # Define the threshold for inactivity (e.g., 72 hours)
        threshold = timezone.now() - timezone.timedelta(seconds=60)

        # Get inactive users
        inactive_users = User.objects.filter(last_activity__lt=threshold)

        print("deleting inactive users")
        # Delete or deactivate inactive users based on your policy
        for user in inactive_users:
            print(f"deleting user: {user.username}")
            # Delete user or deactivate as needed
            user.delete()
