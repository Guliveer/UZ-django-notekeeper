from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('notes/', views.note_list, name='note_list'),
    path('notes/create/', views.note_create, name='note_create'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/<int:pk>/edit/', views.note_edit, name='note_edit'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),
    path('notes/<int:pk>/publish/', views.note_publish, name='note_publish'),
    path('notes/<int:pk>/unpublish/', views.note_unpublish, name='note_unpublish'),
    path('account/', views.account, name='account'),
    path('register/', views.register, name='register'),
    path('signup/', views.signup, name='signup'),
    path('user/<int:pk>/delete/', views.delete_user, name='delete_user'),
    path('manage/note/<int:pk>/delete/', views.admin_delete_note, name='admin_delete_note'),
    path('manage/notes/', views.admin_note_list, name='admin_note_list'),
    path('note/image/<int:image_id>/delete/', views.note_delete_image, name='note_delete_image'),
]
