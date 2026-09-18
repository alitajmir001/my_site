from django.template import Library
from blog.models import Setting
register=Library()



@register.simple_tag
def get_setting_info():

    try:
        setting = Setting.objects.first()
        print('ok')  # برای این مثال شناسه 1 را در نظر گرفته‌ایم
        return setting
    except Setting.DoesNotExist:
        print('none')
        return None