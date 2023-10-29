from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.list_chat_groups, name="list_chat_groups"),
    path('get_username/', views.get_username, name="get_username"),
    path('check_username/', views.check_username, name='check_username'),
    path('chat/<str:group_name>/', views.chat_room, name='chat'),
    path('add_group/', views.add_chat_group, name="add_group"),
    path('delete_group/<str:group_name>/', views.delete_chat_group, name="delete_group" ),
    path('download_chatlog/', views.download_chatlog, name="download_chatlog"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
