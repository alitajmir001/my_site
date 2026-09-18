from django.urls import path
from blog import views
from django.db import connection
app_name='blog'
urlpatterns=[
path('blog/detail/<slug:Product_slug>/<int:pk>/', views.YourModelDetailView.as_view(), name='product-detail'),
path('blog/index/',views.Index_All_Group.as_view(),name='all_group'),
path('',views.Index_All_Group.as_view(),name='all_group'),
path('blog/category/<int:pk>/',views.Category.as_view(),name='all_group'),
path('blog/category/select_item/<str:name>/',views.Category.as_view(),name='orderby_product'),
path('blog/single_product/<str:product_slug>/<int:pk>/',views.YourModelDetailView.as_view(),name='single_product'),
path('blog/blog_Single/<str:blog_slug>/<int:pk>/',views.Blog_View.as_view(),name='single_blog'),
]