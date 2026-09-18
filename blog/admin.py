from django.contrib import admin
from .models import Product,Setting,Variant,Attribute,Gallery,Blog_Text,Tags_BlogText
from django.utils.html import format_html
from django import forms
from ckeditor.widgets import CKEditorWidget



class GalleryInline(admin.TabularInline):
     extra=0
     model=Gallery

     def display_img_1(self,obj):
          return format_html('<img src="{}" style="height:200px;width:200px"/>',obj.photo1.url)
     def display_img_2(self,obj):
          return format_html('<img src="{}" style="height:200px;width:200px"/>',obj.photo2.url)
     def display_img_3(self,obj):
          return format_html('<img src="{}" style="height:200px;width:200px"/>',obj.photo3.url)
     readonly_fields=['display_img_1','display_img_2','display_img_3']




class VariantAdminInline(admin.TabularInline):
    model=Variant   
    extra=0
    # form=VariantForm   
    def display_color(self,obj):
         return format_html("<div style='background-color:{};width:50px;height:20px'></div>",obj.value)  

    readonly_fields=['display_color']       

       
       
       
class ProductAdminForm(forms.ModelForm):  
    def display_img_1(self,obj):
          return format_html('<img src="{}" style="height:200px;width:200px"/>',obj.file.url)
    readonly_fields=['display_img_1']
    
       
       
       
       
          

class ProductAdmin(admin.ModelAdmin):
    exclude=['seen']
    
       
    list_display=[
       'id','title','consent','price','linq','status','is_active','seen','display_image'
    ]
    search_fields=['title']
    inlines=[VariantAdminInline,GalleryInline]   
    def display_image(self,obj):   
            return format_html('<img src="{}" style="height:200px;width:200px;" />'.format(obj.file.url))
    form=ProductAdminForm
        
            
class AttributeAdmin(admin.ModelAdmin):
     list_display=['id','name']   






class SettingAdmin(admin.ModelAdmin):
    list_display=['header_text','content_h1_slider','display_img']
    
    def display_img(self,obj):
        
         return format_html('<img src="{}" style="width:200px;height:100px"/>'.format(obj.slider.url))

      
class Form_Blog_Text(forms.ModelForm):
     text=forms.CharField(widget=CKEditorWidget())
     tags=forms.CharField(widget=forms.TextInput(attrs={'name':'tags','id':'tags'}))
     class Meta:
          fields='__all__'

class Blog_Text_Admin(admin.ModelAdmin):
     model=Blog_Text
     list_display=['id','title','text','slug','user','seen','display_img']
     search_fields=['title']
     def display_img(self,obj):
          if obj.image:
               return format_html('<img src="{}" style="width:200px;length:200px;"/>',obj.image.url)
          return None
     form=Form_Blog_Text
     def save_model(self, request, obj, form, change):
    # First, let's call the parent class's save_model method
         super().save_model(request, obj, form, change)
    
    # Now, let's save the form and extract the tags
         form.save()
         tags = form.cleaned_data['tags']
         tags = tags.split(' ')
    
    
         Tags_BlogText.objects.filter(blog_text=obj).delete()
    # Loop through each tag and save it
         for tag in tags:
             Tags_BlogText.objects.create(blog_text=obj,name=tag)
        
        # Save the tag
          #    item.save()
     
                    
     
class Admin_Tags_BlobText(admin.ModelAdmin):
     model=Tags_BlogText
     list_display=['name','blog_text','linq']
     search_fields=['name']
    
              
                  
                  
                   
              
              
              






admin.site.register(Product,ProductAdmin)
admin.site.register(Setting,SettingAdmin)
admin.site.register(Attribute,AttributeAdmin)
admin.site.register(Blog_Text,Blog_Text_Admin)
admin.site.register(Tags_BlogText,Admin_Tags_BlobText)