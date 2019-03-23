from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.files.images import get_image_dimensions
from django.forms import EmailField, ModelForm, forms, IntegerField

from .models import Profile


class UserCreationForm(UserCreationForm):
    email = EmailField(required=True, )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class ProfileForm(ModelForm):
    phone_number = IntegerField(required=False, )

    class Meta:
        model = Profile
        fields = ["phone_number"]
