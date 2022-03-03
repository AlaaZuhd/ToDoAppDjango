import datetime

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
from django.db.models import Manager


class TodoItemQuerySet(models.QuerySet):
    def completed_todos(self, user):
        return self.filter(owner=user, is_completed=True)

    def uncompleted_todos(self, user):
        return self.filter(owner=user, is_completed=False)

    def over_due_todos(self, user):
        return self.filter(owner=user, is_completed=False, due_date__lt=datetime.datetime.now())

    def todays_todos(self, user):
        current_datetime = datetime.datetime.now()
        return self.filter(owner=user, due_date__date=current_datetime, due_date__gt=current_datetime)

    def my_todos(self, user):
        return self.filter(owner=user)


class TodoItemManager(models.Manager):
    def get_queryset(self):
        return TodoItemQuerySet(self.model, using=self._db)


class ToDoCategory(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='todo_categories')

    def __str__(self):
        return self.name


class ToDoItem(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=400, blank=True)
    owner = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='todo_items')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField()
    is_completed = models.BooleanField(default=False)# default = False.
    is_important = models.BooleanField()# default = False
    category = models.ForeignKey(ToDoCategory,
                                 on_delete=models.CASCADE,
                                 related_name="todo_items")
    objects = Manager()
    todoItemManager = TodoItemManager()

    class Meta:
        ordering = ('due_date',)

    def __str__(self):
        return self.title
