from .models import UserNew
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = UserNew
        fields = ('username','is_table')

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = UserNew
        fields = ('username','is_table')