from django.forms import ModelForm
from todolist.models import Tasklist

class Taskform(ModelForm):
    class Meta:
        model=Tasklist
        fields=['task','done']