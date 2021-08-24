from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.posts, name='posts'),
    path('<slug:category_slug>/post/<slug:slug>/', views.post, name='post'),
    path('<slug:category_slug>/post/<slug:slug>/', views.detail, name='post_detail'),
    path('post/<slug:slug>/', views.category, name='category_detail'),
    path('search/', views.search, name='search'),
    path('contact/', views.contact_us, name='contact'),

    #CRUD PATHS

    path('create_post/', views.createPost, name="create_post"),
    path('update_post/<slug:slug>/', views.updatePost, name="update_post"),
    path('delete_post/<slug:slug>/', views.deletePost, name="delete_post"),


    path('send_email/', views.sendEmail, name="send_email"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('account/', views.userAccount, name="account"),
    path('update_profile/', views.updateProfile, name="update_profile"),
]
