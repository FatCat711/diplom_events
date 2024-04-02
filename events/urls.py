from django.urls import path
from . import views
app_name = "events"

urlpatterns = [
    path('events', views.EventListView.as_view(), name="list"),
    path('event/<int:pk>/', views.EventDetailView.as_view(), name="detail"),
    path('event/<int:pk>/register/', views.event_register, name="reg"),
    path('event/<int:pk>/update/', views.EditEventView.as_view(), name="update"),
    path('event/create/', views.CreateEventView.as_view(), name="create"),
]
