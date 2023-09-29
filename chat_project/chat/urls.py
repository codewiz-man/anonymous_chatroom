from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_chat_groups, name="list_chat_groups"),
    path('chat/<str:group_name>/', views.chat_room, name='chat_room'),
    path('add_group/', views.add_chat_group, name="add_group"),
    path('delete_group/<str:group_name>/', views.delete_chat_group, name="delete_group" )
]
