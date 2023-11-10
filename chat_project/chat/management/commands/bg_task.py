import time
from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
import threading
from chat.models import ChatUser

def cleanup_users():
    while True:
        now = timezone.now()
        inactive_time = now - timedelta(hours=24)
        inactive_users = ChatUser.objects.filter(last_activity__lt=inactive_time)
        print(f'Removing {inactive_users.count()} inactive users')
        inactive_users.delete()
        time.sleep(10)  # Sleep for 1 hour


class Command(BaseCommand):
    help = 'Remove inactive users after 24 hours'

    def handle(self, *args, **options):
        #print(args)
        print('start' in args)
        #if 'start' in args:
        
        self.stdout.write(self.style.SUCCESS('Starting user cleanup thread...'))
        self.cleanup_thread = threading.Thread(target=cleanup_users)
        self.cleanup_thread.daemon = True
        self.cleanup_thread.start()

        try:
            self.cleanup_thread.join()
        except KeyboardInterrupt:
            self.cleanup_thread.join()

        #elif 'stop' in args:
        #    # Stop the background thread
        #    self.cleanup_thread.join()
        #    self.stdout.write(self.style.SUCCESS('User cleanup thread stopped'))
        #else:
        #    self.stdout.write(self.style.ERROR('Usage: python manage.py remove_inactive_users start|stop'))

        
