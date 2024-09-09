from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User


class MyUserCreationForm(UserCreationForm):
    usable_password = None
    class Meta:
        model = User
        fields = ['name', 'username', 'branch', 'year']
    
    def is_valid(self) -> bool:
        return super().is_valid()

class RoomForm(ModelForm):
    class Meta:
        model =  Room
        fields = '__all__'
        exclude = ['host', 'followers']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
