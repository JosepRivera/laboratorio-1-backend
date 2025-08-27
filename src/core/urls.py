from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_items),
    path("api/items/", views.api_items, name="api_items"),
    path("api/items/<int:item_id>/", views.api_item_detail, name="api_item_detail"),
]
