from django.urls import path, include
from todo import views

urlpatterns = [
    path("<int:pk>/", views.ToDoItemDetailView.as_view(), name="todo-detail"),
    path("delete/<int:pk>/", views.ToDoItemDeleteView.as_view(), name="todo-delete"),
    path("update/<int:pk>/", views.ToDoItemUpdateView.as_view(), name="todo-update"),
    path("update/<int:pk>/<str:is_completed>/", views.toDoItemUpdateIsCompplete, name="todo-is-completed-update"),
    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category-retrieve"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("category/update/<int:pk>/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("category/delete/<int:pk>/", views.CategoryDeleteView.as_view(), name="category-delete"),
    path("create/", views.ToDoItemCreateView.as_view(), name="todo-create"),
    path("<str:search>/", views.ToDoListView.as_view(), name="todo-list"),
]