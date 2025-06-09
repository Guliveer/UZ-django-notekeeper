from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('notes/', views.note_list, name='note_list'),
    path('note/add/', views.note_create, name='note_create'),
    path('note/<int:pk>/edit/', views.note_update, name='note_update'),
    path('note/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('signup/', views.signup, name='signup'),
    path('user/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('manage/note/<int:pk>/delete/', views.admin_delete_note, name='admin_delete_note'),
    path('manage/notes/', views.admin_note_list, name='admin_note_list'),
    path('account/', views.account, name='account'),
]
