from typing import Any
from django.shortcuts import get_object_or_404, render,redirect
from django.urls import reverse
from .models import Product,Variant,Blog_Text,Tags_BlogText
from django.contrib.auth.models import Group
from django.views.generic import DetailView,ListView
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import F

    
class YourModelDetailView(DetailView):
    model = Product
    template_name = 'single.html'
    context_object_name='item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        _slug=self.kwargs['product_slug']
        product = Product.objects.get(id=id)
        product.seen += 1
        product.save()
        context['item'] = product
        attributes={}

        for attribute in product.variant_product.all():
            attributes[attribute.attribute.name]=Variant.objects.filter(product_id=id,attribute_id=attribute.attribute.id)
            
            context['attributes'] = attributes

        return context

        
        





class Index_All_Group(ListView):
    model=Group
    template_name = 'index.html'
    context_object_name = 'context'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slider'] = Product.objects.filter(status='p').order_by('-consent')[:8]
        context['galleri'] = Product.objects.filter(is_active=True,status='d')[:3]
        context['groups']=Group.objects.all()
        context['products']=Product.objects.filter(status='p')
        context['blog']=Blog_Text.objects.filter(statuse='p').order_by('-created')
       
                
        return context



class Category(ListView):
    template_name='categories.html'   
    context_object_name='queryset'
    

    def get_queryset(self):
        if 'pk' in self.kwargs:
            group_pk=self.kwargs['pk']
            self.request.session['group_pk']=group_pk
            queryset=Product.objects.filter(group=group_pk,status='p').order_by('title')
 
        elif 'name' in self.kwargs:
            name=self.kwargs['name']
            group_pk=self.request.session['group_pk']
            queryset=Product.objects.filter(group=group_pk,status='p').order_by('title')
            if name=='price':
               
                queryset=queryset.order_by(F('price').asc())
              

            elif name=='consent':
                
                queryset=queryset.order_by(F('consent').desc())
        paginator=Paginator(queryset,8)
        page=self.request.GET.get('page')
        try:
            queryset=paginator.page(page)
        except PageNotAnInteger:
            queryset=paginator.page(1)
        except EmptyPage:
            queryset=paginator.page(paginator.num_pages)
        # objs={'queryset':queryset,'page':page}
        return queryset






class Blog_View(DetailView):
    model=Blog_Text
    template_name='blog.html'
    context_object_name='item'
    def get_context_data(self,**kwargs):

        context=super().get_context_data(**kwargs)
        blog=Blog_Text.objects.get(id=self.kwargs['pk'],statuse='p')
        blog.seen+=1
        blog.save()
        context['item']=blog
        context['blogs_lasted']=Blog_Text.objects.order_by('-publish')[:4]
        context['tags']=Tags_BlogText.objects.filter(blog_text=blog)
        return context
        
                   
                    
               
        
     
     

