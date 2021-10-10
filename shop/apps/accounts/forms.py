from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    username = forms.CharField(
        label="Username: ",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Вкажіть Ваш Login"
            }
        )
    )

    email = forms.EmailField(
        label="Email: ",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Вкажіть Ваш Email"
            }
        )
    )

    password = forms.CharField(
        label="Choose Password: ",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )
    confirm_password = forms.CharField(
        label="Re-enter Password: ",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Password does not match")

        return cleaned_data

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password'
        )


class LoginForm(forms.Form):
    username = forms.CharField(
        # label="Username:",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Login"
            }
        )
    )
    password = forms.CharField(
        # label="Password:",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password"
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
