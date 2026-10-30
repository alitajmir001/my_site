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
ADMIN_TIMER_ROOM = 0

def master_timer_task():
    """این تابع در یک Thread جداگانه اجرا می‌شود و سایت را قفل نمی‌کند"""
    global ADMIN_TIMER_ROOM
    while True:
        # به جای asyncio.sleep از time.sleep در ترد استفاده می‌کنیم
        time.sleep(1)
        ADMIN_TIMER_ROOM += 1
        # برای تست در کنسول (در Render این را در لاگ‌ها می‌بینید)
        # print(f"Timer Tick: {ADMIN_TIMER_ROOM}")

class YourAppNameConfig(AppConfig): # نام اپلیکیشن خود را جایگزین کنید
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'your_app_name' # نام اپلیکیشن خود را اینجا بنویسید

    def ready(self):
        """
        این متد توسط جنگو بلافاصله پس از بالا آمدن اپلیکیشن فراخوانی می‌شود.
        """
        # ایجاد یک ترد (Thread) جداگانه برای اجرای تایمر
        # استفاده از daemon=True باعث می‌شود با بسته شدن سرور، این ترد هم بسته شود
        timer_thread = threading.Thread(target=master_timer_task, daemon=True)
        timer_thread.start()
