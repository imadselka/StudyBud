from django.forms import ModelForm
from .models import Room, Message


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"


from django import forms


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ("body",)  # Note the use of parentheses instead of square brackets
