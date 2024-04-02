from django.urls import path
from . import views
app_name = "core"

urlpatterns = [
    path('', views.BaseView.as_view(), name="home"),
]
