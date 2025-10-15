from django.urls import path
from . import views

app_name = 'incident'

urlpatterns = [
    path('', views.incident_list, name='list'),
    path('new-incident/', views.incident_new, name='new-incident'),
    path('manager-dashboard/', views.manager_dashboard, name='manager-dashboard'),
    path('<slug:slug>', views.incident_page, name='page'),
    path('<slug:slug>/update-status/', views.incident_update_status, name='update-status'),
]