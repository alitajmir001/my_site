from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User,Group
from django.dispatch import receiver
from django.db.models.signals import pre_delete

class Product(models.Model):
    STATUS=(('p','publeshed'),('d','draft'))
    title=models.CharField(max_length=150,verbose_name='عنوان')
    slug=models.CharField(max_length=200,null=True,verbose_name='اسلاگ') 
    price=models.CharField(max_length=15,verbose_name='قیمت')
    descryption=models.TextField(blank=True,verbose_name='توضیحات')
    linq=models.URLField(verbose_name='لینک')
    alt=models.CharField(max_length=50)
    consent=models.FloatField(blank=True,null=True,verbose_name='میزان رضایتمندی مشتری ها')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    publish=models.DateTimeField(null=True,blank=True,verbose_name='زمان انتشار')
    file=models.ImageField(upload_to='images/product',verbose_name='عکس')
    group=models.ForeignKey(Group,on_delete=models.CASCADE,related_name='product',verbose_name='گروه')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='product',verbose_name='نام کاربر')
    status=models.CharField(max_length=1,choices=STATUS,default='draft',verbose_name='وضعیت انتشار')
    is_active=models.BooleanField(default=False,null=True,verbose_name='نمایش در گالری')
    seen=models.IntegerField(default=0,null=True,blank=True,verbose_name='تعداد بازدید')
   
    def get_absolute_url(self):
        return reverse('blog:product-detail',args=[str(self.slug),self.id])
    
    class Meta:
        verbose_name='محصول'
        verbose_name_plural='محصولات'

    def __str__(self):
        return self.title


@receiver(pre_delete,sender=Product)
def delete_image(sender,instance, **kwargs):
    if instance.file:
        instance.file.delete(False)




class Attribute(models.Model):
    name=models.CharField(max_length=100)
    def __str__(self):
        return self.name


    

class Variant(models.Model):
    attribute=models.ForeignKey(Attribute,on_delete=models.CASCADE,null=True,related_name='variant_attribute',blank=True)
    value=models.CharField(max_length=50)
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,related_name='variant_product',null=True)

   


class Gallery(models.Model):
    photo1=models.ImageField(upload_to='images/gallery/')
    photo2=models.ImageField(upload_to='images/gallery/')
    photo3=models.ImageField(upload_to='images/gallery/')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='gallery')

    class Meta:
        verbose_name='گالری'
        verbose_name_plural='گالری ها'







class Setting(models.Model):
    header_text=models.CharField(max_length=25,verbose_name='متن هدر سایت')   
    content_h1_slider=models.CharField(max_length=25,verbose_name='متن بزرگ اسلایدر')
    slider=models.ImageField(upload_to='images/slider')
    class Meta:
        verbose_name='تنظیمات'
        verbose_name_plural='تنظیمات'



class Blog_Text(models.Model):
    STATUS_PUBLISH=(('p','publish'),('d','draft'))
    title=models.CharField(max_length=100,verbose_name='عنوان')
    text=models.TextField(verbose_name='متن')
    image=models.ImageField(upload_to='images/blog',null=True,blank=True,verbose_name='تصویر')
    slug=models.CharField(max_length=200,null=True,verbose_name='اسلاگ')
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_text',verbose_name='نام کاربر')
    created=models.DateTimeField(auto_now_add=True)
    seen=models.IntegerField(default=0,null=True,blank=True,verbose_name='تعداد بازدید')
    publish=models.DateTimeField(null=True,blank=True,verbose_name='زمان انتشار')
    statuse=models.CharField(max_length=1,choices=STATUS_PUBLISH,default='draft',verbose_name='وضعیت انتشار')
    
    def __str__(self):
        return self.title


@receiver(pre_delete,sender=Blog_Text)
def delete_image(sender,instance, **kwargs):
    if instance.image:
        instance.image.delete(False)




class Tags_BlogText(models.Model):
    name=models.CharField(max_length=50)
    blog_text=models.ForeignKey(Blog_Text,on_delete=models.CASCADE,related_name='tags_blogtext')
    linq=models.URLField(null=True)
    

    


