#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.contrib.auth import get_user_model
from django.db import connection
from django.core.management import call_command
def main():
    

    # بررسی می‌کنیم اگر کاربر وجود ندارد، بسازیمش
    try:
        
        User = get_user_model()
        if not User.objects.filter(username='admin299').exists():
            # این دستور را با دقت کپی کن
            
            
            call_command('createsuperuser', username='admin299', email='admin@example.com', password='3131', interactive=False)
            print("✅ Superuser created automatically!")
        else:
            call_command('migrate', interactive=False)
    except Exception as e:
        # اگر هنوز اپ‌ها لود نشده باشند، این خطا را نادیده بگیر و اجازه بده سرور بالا بیاید
        print(f"ℹ️ Info: {e}")
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
   


if __name__ == '__main__':
    main()
