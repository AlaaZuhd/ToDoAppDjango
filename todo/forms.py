import datetime

from django import forms
from .models import ToDoItem, ToDoCategory


class UpdateToDoItemForm(forms.ModelForm):

    class Meta:
        model = ToDoItem
        fields = "__all__"
        exclude = ('owner', )

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get("due_date")
        is_completee = cleaned_data.get('is_completed')
        if not is_completee:
            current_date = datetime.datetime.now()
            d = datetime.datetime(due_date.year, due_date.month, due_date.day, hour=due_date.hour, minute=due_date.minute, second=due_date.second,
                    microsecond=due_date.microsecond, tzinfo=None, fold=0)
            if d <= current_date:
                raise forms.ValidationError(
                    "Due Date can't be in the past."
                )




class CreateToDoItemForm(forms.ModelForm):

    class Meta:
        model = ToDoItem
        fields = "__all__"
        exclude = ('owner', 'is_completed', )

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get("due_date")
        current_date = datetime.datetime.now()
        d = datetime.datetime(due_date.year, due_date.month, due_date.day, hour=due_date.hour, minute=due_date.minute, second=due_date.second,
                microsecond=due_date.microsecond, tzinfo=None, fold=0)
        if d <= current_date:
            raise forms.ValidationError(
                "Due Date can't be in the past."
            )


class CategoryForm(forms.ModelForm):

    class Meta:
        model = ToDoCategory
        fields = "__all__"
        exclude = ('owner', )