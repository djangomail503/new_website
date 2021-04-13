from django.forms import ModelForm
from django.contrib.auth.models import User
from blog_app import models
class UserRegisterForm(ModelForm):
    class Meta():
        model = User
        fields = ('username', 'email', 'password')

class PostCommentForm(ModelForm):
    class Meta():
        model = models.Comment
        exclude = ('post',)