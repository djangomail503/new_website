from django.urls import path, include
from blog_app import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('post/create/', views.PostCreateView.as_view(), name = 'post_create'),

    path('post/published/', views.PostListView.as_view(), name = 'post_list'),

    path('post/drafts/', views.PostDraftView.as_view(), name = 'post_draft'),

    path('post/detail/<int:pk>', views.PostDetailView.as_view(), name = 'post_detail'),

    path('post/update/<int:pk>', views.PostUpdateView.as_view(), name = 'post_update'),

    path('post/delete/<int:pk>', views.PostDeleteView.as_view(), name = 'post_delete'),

    path("post_publish/<int:pk>", views.publish_post, name = 'publish'),
    path("comment/create/<int:pk>", views.add_comment, name = 'comments'),
    

]

