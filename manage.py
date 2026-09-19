#!/usr/bin/env python
import os
import sys
import django

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    
    # حتماً باید این خط را اضافه کنید تا جنگو بالا بیاید
    try:
        django.setup()
    except Exception:
        pass 

    from django.core.management import call_command
    from django.contrib.auth import get_user_model

    # ۱. اجرای مهاجرت‌ها (Migrations)
    try:
        print("Running migrations...")
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Error migrating: {e}")

    # ۲. ساخت ادمین
    try:
        User = get_user_model()
        if not User.objects.filter(username='admin299').exists():
            print("Creating superuser...")
            call_command('createsuperuser', username='admin299', email='admin@example.com', password='GAPGPTMASKTOKENcs82jfrxajX0X', interactive=False)
            print("✅ Superuser created!")
    except Exception as e:
        print(f"Error creating superuser: {e}")

    # ۳. اجرای دستور اصلی جنگو
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django...") from exc
    
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
