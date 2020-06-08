from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image, Category

class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = "Min. 8 characters long.<br>"
        self.fields['username'].help_text = "Max. 150 characters."
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class ImageForm(forms.Form):
    image = forms.ImageField()
    description = forms.CharField(widget=forms.Textarea)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)
    
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['class'] = 'file-input'
     

class CategoryForm(forms.Form):
    name = forms.CharField()