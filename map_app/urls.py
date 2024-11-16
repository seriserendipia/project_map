from django.urls import path
from . import views

app_name = 'map_app'

# URL patterns for the map application
urlpatterns = [
    path('', views.MapView.as_view(), name='map'),  # Main map view
    path('add_point/', views.add_point, name='add_point'),  # Add new point
    path('test-connection/', views.test_db_connection, name='test_connection'),  # Test database connection
    path('test/', views.test_view, name='test'),  # Test view
    path('delete-point/<int:point_id>/', views.delete_point, name='delete_point'),  # Delete point
] 