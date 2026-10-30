from django.apps import AppConfig
import threading
import time


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name='وبلاگ'



# اگر می‌خواهید این مقدار در کل سایت قابل دسترسی باشد، 
# بهتر است آن را در دیتابیس ذخیره کنید. 
# اما برای تست، فعلاً در سطح ماژول نگه می‌داریم.


# این متغیر خارج از کلاس تعریف می‌شود تا در سطح ماژول باشد
ADMIN_TIMER_ROOM = 0

def master_timer_task():
    """این تابع در یک Thread جداگانه اجرا می‌شود"""
    global ADMIN_TIMER_ROOM
    while True:
        time.sleep(1)
        ADMIN_TIMER_ROOM += 1
        # نکته: این مقدار فقط در حافظه این سرور است و با ریست شدن سرور صفر می‌شود.

class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = 'وبلاگ'

    def ready(self):
        """اجرای تایمر فقط یکبار در هنگام استارت آپ"""
        # استفاده از threading برای جلوگیری از قفل شدن سرور
        timer_thread = threading.Thread(target=master_timer_task, daemon=True)
        timer_thread.start()
