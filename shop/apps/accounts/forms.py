from django import forms
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):

    username = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                "class": "form-control-lg",
                "placeholder": "Ваш логін"
            }
        )
    )

    email = forms.EmailField(
        label='',
        widget=forms.TextInput(
            attrs={
                "class": "form-control-lg",
                "placeholder": "Ваш Email"
            }
        )
    )

    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control-lg",
                "placeholder": "Вакжіть пароль"
            }
        ),
    )
    confirm_password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control-lg",
                "placeholder": "Повторіть пароль"
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
        label='',
        widget=forms.TextInput(
            attrs={
                "class": "form-control-lg",
                "placeholder": "Логін"
            }
        )
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control-lg",
                "placeholder": "Пароль"
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
