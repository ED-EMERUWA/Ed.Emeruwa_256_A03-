from django.urls import path
from . import views

urlpatterns = [
    path('', views.current_event_list, name='event_list'),
    path('all_events', views.all_events_list, name='all_events_list'),
    path('register/<int:event_id>/', views.register_for_event, name='register_event'),
    path('unregister/<int:event_id>/', views.unregister_from_event, name='unregister_event'),
    path('all_users', views.user_list, name='user_list'),
    path('create/', views.create_event, name='create_event'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('delete/<int:event_id>/', views.confirm_delete_event, name='confirm_delete_event'),
    path('delete/<int:event_id>/confirm/', views.delete_event, name='delete_event'),

]
