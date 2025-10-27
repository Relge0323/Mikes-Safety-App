from django.urls import path
from . import views

app_name = 'incident'

urlpatterns = [
    path('', views.incident_list, name='list'),
    path('new-incident/', views.incident_new, name='new-incident'),
    path('my-incidents/', views.my_incidents, name='my-incidents'),
    path('notifications/', views.notifications_list, name='notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_read, name='mark-notification-read'),
    path('notifications/mark-all-read/', views.mark_all_notifications_read, name='mark-all-read'),
    path('manager-dashboard/', views.manager_dashboard, name='manager-dashboard'),
    path('<slug:slug>/', views.incident_page, name='page'),
    path('<slug:slug>/update-status/', views.incident_update_status, name='update-status'),
]