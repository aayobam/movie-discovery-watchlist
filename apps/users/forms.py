from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model, forms as auth_forms


class CustomUserCreationForm(auth_forms.UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


class CustomUserChangeForm(auth_forms.UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)


class UserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ('date_joined', 'profile_code')
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control mt-3", "placeholder": "Enter email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter last name"}),
            "gender": forms.Select(attrs={"class": "form-control mt-3"}),
            "phone_no": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter phone_no"}),
            "password": forms.PasswordInput(attrs={"class": "form-control mt-3", "placeholder": "Enter password"}),
            "address": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter address"}),
            "city": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter city"}),
            "state": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter state"}),
            "country": forms.Select(attrs={"class": "form-control mt-3"}),
            "document_type": forms.Select(attrs={"class": "form-control mt-3"}),
            "document": forms.FileInput(attrs={"class": "form-control mt-3"}),
            "profile_picture": forms.FileInput(attrs={"class": "form-control mt-3"}),
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(widget=forms.EmailInput, required=False)
    phone_no = forms.CharField(max_length=14, required=False)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email',
                  'phone_no', 'address', 'city', 'state']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['last_name'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['phone_no'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['address'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['city'].widget.attrs.update({"class": "form-control mb-3"})
        self.fields['state'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['profile_picture'].widget.attrs.update(
            {"class": "form-control mb-3"})


class CustomPasswordConfirmForm(auth_forms.PasswordChangeForm):
    old_password = None
