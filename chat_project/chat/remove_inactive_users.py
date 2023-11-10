from datetime import timedelta
import time
import threading
from django.utils import timezone

from chat.models import ChatUser


def cleanup_users():
    print("starting remove inactive users task")
    INACTIVE_HOURS = 24
    RUN_EVERY_SECS = 3600
    while True:
        now = timezone.now()
        inactive_time = now - timedelta(hours=INACTIVE_HOURS)
        inactive_users = ChatUser.objects.filter(last_activity__lt=inactive_time)
        print(f'Removing {inactive_users.count()} inactive users')
        inactive_users.delete()
        time.sleep(RUN_EVERY_SECS)  # Sleep for 1 hour

bgtask_running = False

def start_bgtask():
    th = threading.Thread(target=cleanup_users)
    th.daemon = True
    th.start()

