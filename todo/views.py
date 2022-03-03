from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from .forms import UpdateToDoItemForm, CategoryForm, CreateToDoItemForm
from .models import ToDoItem, ToDoCategory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class ToDoListView(LoginRequiredMixin, ListView):
    template_name = "todo/todo_list.html"
    login_url = '/users/login/'

    def get_queryset(self):
        search = self.kwargs.get('search')
        if search == 'today':
            return ToDoItem.todoItemManager.all().todays_todos(self.request.user).all()
        elif search == 'completed':
            return ToDoItem.todoItemManager.all().completed_todos(self.request.user).all()
        elif search == 'uncompleted':
            return ToDoItem.todoItemManager.all().uncompleted_todos(self.request.user).all()
        elif search == 'overdue':
            return ToDoItem.todoItemManager.all().over_due_todos(self.request.user).all()
        else:
            return ToDoItem.todoItemManager.all().my_todos(self.request.user)


# from django.contrib.auth.mixins import UserPassesTestMixin

class ToDoItemDetailView(LoginRequiredMixin, DetailView):
    model = ToDoItem
    template_name = 'todo/todoitem_detail.html'

    def get_object(self, queryset=None):
        try:
            return ToDoItem.todoItemManager.all().my_todos(self.request.user).get(id=self.kwargs['pk'])
        except Exception as e:
            return []

# if not the owner then how to handel it effectively.
class ToDoItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ToDoItem
    success_url = '/todo/today/'
    template_name = 'todo/todoitem_confirm_delete.html'

    def get_queryset(self):
        return ToDoItem.todoItemManager.all().my_todos(self.request.user)

    def test_func(self):
        return self.get_object().owner_id == self.request.user.pk


class ToDoItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ToDoItem
    template_name = 'todo/todoitem_update_form.html'
    form_class = UpdateToDoItemForm

    def get_success_url(self):
        return reverse('todo-detail', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        return ToDoItem.todoItemManager.all().my_todos(self.request.user)

    def test_func(self):
        return self.get_object().owner_id == self.request.user.pk


class ToDoItemCreateView(CreateView):
    model = ToDoItem
    template_name = "todo/add_todoitem.html"
    form_class = CreateToDoItemForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return '/todo/' + str(self.get_form().instance.id) + "/"


def toDoItemUpdateIsCompplete(request, pk, is_completed):
    try:
        obj = ToDoItem.todoItemManager.all().my_todos(request.user).get(id=pk)
        obj.is_completed = is_completed
        obj.save()
    except Exception as e:
        pass # i can add a message..
    return redirect(request.META.get('HTTP_REFERER'))


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = ToDoCategory
    template_name = "todo/add_category.html"
    form_class = CategoryForm
    success_url = "/dashboard/"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "todo/categories_list.html"
    login_url = '/users/login/'

    def get_queryset(self):
        return ToDoCategory.objects.filter(owner=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ToDoCategory
    success_url = '/todo/category/'
    template_name = 'todo/category_confirm_delete.html'

    def get_queryset(self):
        return ToDoCategory.objects.filter(owner=self.request.user)


    def test_func(self):
        return self.get_object().owner_id == self.request.user.pk


class CategoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ToDoCategory
    template_name = 'todo/category_update_form.html'
    form_class = CategoryForm

    def get_success_url(self):
        return reverse('category-retrieve', kwargs={'pk': self.kwargs['pk']})

    def get_queryset(self):
        return ToDoCategory.objects.filter(owner=self.request.user)

    def test_func(self):
        return self.get_object().owner_id == self.request.user.pk


class CategoryDetailView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ToDoItem
    template_name = 'todo/category_detail.html'

    def get_queryset(self):
        return ToDoCategory.objects.filter(owner=self.request.user, id=self.kwargs['pk'])

    def test_func(self):
        return self.get_object().owner_id == self.request.user.pk

