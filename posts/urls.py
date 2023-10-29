from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('all', views.PostListView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    path('post-delete/<int:pk>/', views.PostDeleteView.as_view(), name='post-delete'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('post-update/<int:pk>/', views.PostUpdateView.as_view(), name='post-update'),

    path('category/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('category-delete/<int:pk>/', views.CategoryDeleteView.as_view(), name='category-delete'),
    # path('category-create/', views.CategoryCreateView.as_view(), name='category-create'),
]